package uk.ramp.api;

import static java.nio.file.StandardOpenOption.CREATE;
import static java.nio.file.StandardOpenOption.READ;
import static java.nio.file.StandardOpenOption.WRITE;

import java.io.IOException;
import java.io.UncheckedIOException;
import java.lang.ref.Cleaner;
import java.lang.ref.Cleaner.Cleanable;
import java.nio.channels.FileChannel;
import java.nio.file.Path;
import java.time.Clock;
import java.time.Instant;
import java.util.Map;
import uk.ramp.access.AccessLogger;
import uk.ramp.access.AccessLoggerFactory;
import uk.ramp.config.Config;
import uk.ramp.config.ConfigFactory;
import uk.ramp.file.CleanableFileChannel;
import uk.ramp.hash.HashMetadataAppender;
import uk.ramp.hash.Hasher;
import uk.ramp.metadata.MetadataFactory;
import uk.ramp.metadata.MetadataItem;
import uk.ramp.metadata.MetadataSelector;
import uk.ramp.metadata.ReadOnlyRunMetadata;
import uk.ramp.metadata.WriteOnlyRunMetadata;
import uk.ramp.overrides.OverridesApplier;
import uk.ramp.yaml.YamlFactory;

/**
 * Java implementation of Data Pipeline File API.
 *
 * <p>Users should initialise this library using a try-with-resources block or ensure that .close()
 * is explicitly closed when the required file handles have been accessed.
 *
 * <p>As a safety net, .close() is called by a cleaner when the instance of FileApi is being
 * collected by the GC.
 */
public class FileApi implements AutoCloseable {
  private static final Cleaner cleaner = Cleaner.create(); // safety net for closing
  private final Cleanable cleanable;
  private final MetadataSelector metadataSelector;
  private final CleanableAccessLogger accessLoggerWrapper;
  private final OverridesApplier overridesApplier;
  private final HashMetadataAppender hashMetadataAppender;
  private final boolean shouldVerifyHash;
  private final WriteOnlyRunMetadata runMetadata;

  public FileApi(Path configFilePath) {
    this(Clock.systemUTC(), configFilePath);
  }

  FileApi(Clock clock, Path configFilePath) {
    var openTimestamp = clock.instant();
    var hasher = new Hasher();
    var yamlReader = new YamlFactory().yamlReader();
    var runMetadata = new MetadataFactory().runMetadata();
    var config = new ConfigFactory().config(yamlReader, hasher, openTimestamp, configFilePath);
    this.overridesApplier = new OverridesApplier(config);
    this.accessLoggerWrapper =
        new CleanableAccessLogger(
            new AccessLoggerFactory(),
            config,
            new YamlFactory(),
            clock,
            openTimestamp,
            hasher,
            runMetadata);
    this.runMetadata = runMetadata;
    this.cleanable = cleaner.register(this, accessLoggerWrapper);
    this.metadataSelector =
        new MetadataFactory()
            .metadataSelector(new YamlFactory().yamlReader(), config.normalisedDataDirectory());
    this.hashMetadataAppender = new HashMetadataAppender(hasher);
    this.shouldVerifyHash = config.failOnHashMisMatch();
  }

  // Defining a resource that requires cleaning
  private static class CleanableAccessLogger implements Runnable {
    private final AccessLogger accessLogger;

    CleanableAccessLogger(
        AccessLoggerFactory accessLoggerFactory,
        Config config,
        YamlFactory yamlFactory,
        Clock clock,
        Instant openTimestamp,
        Hasher hasher,
        ReadOnlyRunMetadata runMetadata) {
      this.accessLogger =
          accessLoggerFactory.accessLogger(
              config, yamlFactory.yamlWriter(), clock, openTimestamp, hasher, runMetadata);
    }

    // Invoked by close method or cleaner
    @Override
    public void run() {
      accessLogger.writeAccessEntries();
    }
  }

  /**
   * Return file for reading corresponding to the given metadata. The file contents are hashed, and
   * a record is made of the read.
   *
   * @return FileChannel for input
   * @param query input query
   */
  public CleanableFileChannel openForRead(MetadataItem query) {
    try {
      return openForReadCheckedExc(query);
    } catch (IOException e) {
      throw new UncheckedIOException(e);
    }
  }

  private CleanableFileChannel openForReadCheckedExc(MetadataItem query) throws IOException {
    var overriddenQuery = overridesApplier.applyReadOverrides(query);
    var metaDataItem = metadataSelector.find(overriddenQuery);
    var normalisedFilename = metaDataItem.normalisedFilename();
    var hashedMetaDataItem = hashMetadataAppender.addHash(metaDataItem, shouldVerifyHash);
    accessLoggerWrapper.accessLogger.logRead(query, hashedMetaDataItem);
    return new CleanableFileChannel(FileChannel.open(Path.of(normalisedFilename), READ), () -> {});
  }

  /**
   * Return matching file for update corresponding to the given metadata. When the file is closed
   * the file contents are hashed, and a record is made of the write.
   *
   * @return FileChannel for output
   * @param query input query
   */
  public CleanableFileChannel openForWrite(MetadataItem query) {
    try {
      return openForWriteChecked(query);
    } catch (IOException e) {
      throw new UncheckedIOException(e);
    }
  }

  private CleanableFileChannel openForWriteChecked(MetadataItem query) throws IOException {
    var overriddenQuery = overridesApplier.applyWriteOverrides(query);
    var normalisedFilename = overriddenQuery.normalisedFilename();
    Runnable onClose = () -> executeOnCloseFileHandle(query, overriddenQuery);
    return new CleanableFileChannel(
        FileChannel.open(Path.of(normalisedFilename), CREATE, WRITE), onClose);
  }

  private void executeOnCloseFileHandle(MetadataItem queryMeta, MetadataItem accessedMeta) {
    var hashedAccessedMeta = hashMetadataAppender.addHash(accessedMeta, false);
    accessLoggerWrapper.accessLogger.logWrite(queryMeta, hashedAccessedMeta);
  }

  /**
   * A way to pass in additional metadata into the access log which is written out when the File API
   * session is closed. It is important to note that this additional metadata is not used to
   * determine the file handle to use when reading or writing.
   *
   * @param additionalMetadata extra metadata which will be logged in the access log.
   */
  public void setRunMetadata(Map<String, String> additionalMetadata) {
    runMetadata.update(additionalMetadata);
  }

  /** Close the session and write the access log. */
  @Override
  public void close() {
    cleanable.clean();
  }
}
