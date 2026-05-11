package selftest

import "testing"

func TestRun_AllModesPass(t *testing.T) {
	code, msg := Run(ModeAll)
	if code != 0 {
		t.Fatalf("ModeAll: code=%d msg=%s", code, msg)
	}
}

func TestRun_EmptyModeIsAll(t *testing.T) {
	code, _ := Run("")
	if code != 0 {
		t.Fatalf("empty mode should equal ModeAll, got %d", code)
	}
}

func TestRun_UnknownModeReturnsExit2(t *testing.T) {
	code, msg := Run("not-a-mode")
	if code != 2 {
		t.Fatalf("unknown mode should be exit 2, got %d (%s)", code, msg)
	}
}

func TestRun_IndividualModesPass(t *testing.T) {
	modes := []Mode{ModeFlagDeclared, ModeR5Vacuous, ModePerModeFixture, ModeExitCodeContract, ModeHarnessDeclaration}
	for _, m := range modes {
		t.Run(string(m), func(t *testing.T) {
			code, msg := Run(m)
			if code != 0 {
				t.Fatalf("%s: code=%d msg=%s", m, code, msg)
			}
		})
	}
}

func TestPerModeFixture_DetectsAllRuntimes(t *testing.T) {
	if code, msg := checkPerModeFixture(); code != 0 {
		t.Fatalf("checkPerModeFixture: %d %s", code, msg)
	}
}

func TestExitCodeContract(t *testing.T) {
	if code, msg := checkExitCodeContract(); code != 0 {
		t.Fatalf("contract: %d %s", code, msg)
	}
}
