// Fixture file — AC-ADS-06 T-02 negative proof.
// This file MUST be rejected by check-ads-boundaries.py --check ac-ads-06.
import { AppShell } from "src/components/app/AppShell";

export default function MarketingLanding() {
  return <AppShell><div>marketing landing (forbidden composition)</div></AppShell>;
}
