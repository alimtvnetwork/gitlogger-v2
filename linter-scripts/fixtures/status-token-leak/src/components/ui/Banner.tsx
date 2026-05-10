// Fixture file — AC-ADS-10 T-02 negative proof.
// References --app-status-error from §07 territory → MUST be rejected.
export const Banner = () => (
  <div style={{ color: "var(--app-status-error)" }}>error banner (forbidden)</div>
);
