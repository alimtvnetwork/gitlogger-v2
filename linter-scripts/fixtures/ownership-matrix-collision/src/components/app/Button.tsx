// Fixture file — AC-ADS-09 T-03 negative proof.
// Collides with src/components/ui/Button.tsx → MUST be rejected.
import { Button as UiButton } from "../ui/Button";
export const Button = () => UiButton(); // colliding name in §24 territory
