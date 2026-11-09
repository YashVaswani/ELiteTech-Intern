import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import PredictForm from "./PredictForm";

describe("PredictForm", () => {
  beforeEach(() => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: true,
        json: async () => ({ cluster: 0, segment: "Champions" }),
      }),
    );
  });

  it("submits RFM values and shows the predicted segment", async () => {
    render(<PredictForm />);

    fireEvent.click(screen.getByRole("button", { name: /classify/i }));

    await waitFor(() => {
      expect(screen.getByText(/Champions/)).toBeInTheDocument();
    });

    expect(fetch).toHaveBeenCalledWith("/api/predict", expect.objectContaining({ method: "POST" }));
  });

  it("shows an error message when the request fails", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: false,
        status: 422,
        statusText: "Unprocessable Entity",
        json: async () => ({ detail: "frequency must be greater than 0" }),
      }),
    );

    render(<PredictForm />);
    fireEvent.click(screen.getByRole("button", { name: /classify/i }));

    await waitFor(() => {
      expect(screen.getByText(/frequency must be greater than 0/)).toBeInTheDocument();
    });
  });
});
