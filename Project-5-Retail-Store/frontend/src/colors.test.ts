import { describe, expect, it } from "vitest";
import { colorForCluster } from "./colors";

describe("colorForCluster", () => {
  it("is deterministic for the same cluster id", () => {
    expect(colorForCluster(2)).toBe(colorForCluster(2));
  });

  it("gives different clusters different colors within palette range", () => {
    expect(colorForCluster(0)).not.toBe(colorForCluster(1));
  });

  it("wraps around for cluster ids beyond the palette size", () => {
    expect(colorForCluster(0)).toBe(colorForCluster(8));
  });
});
