package uk.ramp.metadata;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import org.junit.Test;

public class MetadataItemTest {

  @Test
  public void testIsSuperSetOfWithEqualFilename() {
    var meta1 = ImmutableMetadataItem.builder().internalFilename("filename").build();
    var meta2 = ImmutableMetadataItem.builder().internalFilename("filename").build();

    assertThat(meta1.isSuperSetOf(meta2)).isTrue();
  }

  @Test
  public void testIsSuperSetOfWithEqualDataProduct() {
    var meta1 = ImmutableMetadataItem.builder().dataProduct("dataProduct").build();
    var meta2 = ImmutableMetadataItem.builder().dataProduct("dataProduct").build();

    assertThat(meta1.isSuperSetOf(meta2)).isTrue();
  }

  @Test
  public void testIsSuperSetOfWithEqualExtension() {
    var meta1 = ImmutableMetadataItem.builder().extension("ext").build();
    var meta2 = ImmutableMetadataItem.builder().extension("ext").build();

    assertThat(meta1.isSuperSetOf(meta2)).isTrue();
  }

  @Test
  public void testIsSuperSetOfWithEqualVersion() {
    var meta1 = ImmutableMetadataItem.builder().internalVersion("version").build();
    var meta2 = ImmutableMetadataItem.builder().internalVersion("version").build();

    assertThat(meta1.isSuperSetOf(meta2)).isTrue();
  }

  @Test
  public void testIsSuperSetOfPartialVersion() {
    var queryKey = ImmutableMetadataItem.builder().build();
    var otherKey = ImmutableMetadataItem.builder().internalVersion("version").build();

    assertThat(otherKey.isSuperSetOf(queryKey)).isTrue();
    assertThat(queryKey.isSuperSetOf(otherKey)).isFalse();
  }

  @Test
  public void testIsSuperSetOfPartialFilename() {
    var queryKey = ImmutableMetadataItem.builder().build();
    var otherKey = ImmutableMetadataItem.builder().internalFilename("filename").build();

    assertThat(otherKey.isSuperSetOf(queryKey)).isTrue();
    assertThat(queryKey.isSuperSetOf(otherKey)).isFalse();
  }

  @Test
  public void testIsSuperSetOfPartialFilenameAndVersion() {
    var queryKey = ImmutableMetadataItem.builder().build();
    var otherKey =
        ImmutableMetadataItem.builder()
            .internalFilename("filename")
            .internalVersion("version")
            .build();

    assertThat(otherKey.isSuperSetOf(queryKey)).isTrue();
    assertThat(queryKey.isSuperSetOf(otherKey)).isFalse();
  }

  @Test
  public void testIsSuperSetOfFilenameAndVersionNotMatching() {
    var queryKey = ImmutableMetadataItem.builder().internalFilename("filename").build();
    var otherKey = ImmutableMetadataItem.builder().internalVersion("version").build();

    assertThat(otherKey.isSuperSetOf(queryKey)).isFalse();
    assertThat(queryKey.isSuperSetOf(otherKey)).isFalse();
  }

  @Test
  public void testIsSuperSetOfIssuesEqual() {
    List<IssueItem> issues =
        List.of(ImmutableIssueItem.builder().severity(1).description("desc").build());
    var meta1 = ImmutableMetadataItem.builder().issues(issues).build();
    var meta2 = ImmutableMetadataItem.builder().issues(issues).build();

    assertThat(meta1.isSuperSetOf(meta2)).isTrue();
  }

  @Test
  public void testIsSuperSetOfIssuesPartial() {
    List<IssueItem> issues =
        List.of(ImmutableIssueItem.builder().severity(1).description("desc").build());
    var queryKey = ImmutableMetadataItem.builder().build();
    var otherKey = ImmutableMetadataItem.builder().issues(issues).build();

    assertThat(otherKey.isSuperSetOf(queryKey)).isTrue();
    assertThat(queryKey.isSuperSetOf(otherKey)).isFalse();
  }

  @Test
  public void testIsSuperSetOfIssuesNotMatchingSeverity() {
    List<IssueItem> issues1 =
        List.of(ImmutableIssueItem.builder().severity(1).description("desc").build());
    List<IssueItem> issues2 =
        List.of(ImmutableIssueItem.builder().severity(2).description("desc").build());
    var queryKey = ImmutableMetadataItem.builder().issues(issues1).build();
    var otherKey = ImmutableMetadataItem.builder().issues(issues2).build();

    assertThat(otherKey.isSuperSetOf(queryKey)).isFalse();
    assertThat(queryKey.isSuperSetOf(otherKey)).isFalse();
  }

  @Test
  public void testIsSuperSetOfIssuesNotMatchingDescription() {
    List<IssueItem> issues1 =
        List.of(ImmutableIssueItem.builder().severity(1).description("desc 1").build());
    List<IssueItem> issues2 =
        List.of(ImmutableIssueItem.builder().severity(1).description("desc 2").build());
    var queryKey = ImmutableMetadataItem.builder().issues(issues1).build();
    var otherKey = ImmutableMetadataItem.builder().issues(issues2).build();

    assertThat(otherKey.isSuperSetOf(queryKey)).isFalse();
    assertThat(queryKey.isSuperSetOf(otherKey)).isFalse();
  }

  @Test
  public void testIsSuperSetOfNamespace() {
    var queryKey = ImmutableMetadataItem.builder().build();
    var otherKey = ImmutableMetadataItem.builder().namespace("ns").build();

    assertThat(otherKey.isSuperSetOf(queryKey)).isTrue();
    assertThat(queryKey.isSuperSetOf(otherKey)).isFalse();
  }

  @Test
  public void testIsSuperSetOfDescription() {
    var queryKey = ImmutableMetadataItem.builder().build();
    var otherKey = ImmutableMetadataItem.builder().description("desc").build();

    assertThat(otherKey.isSuperSetOf(queryKey)).isTrue();
    assertThat(queryKey.isSuperSetOf(otherKey)).isFalse();
  }
}
