import { useEffect } from "react";
import { PageShell } from "../../components/PageShell";

/**
 * Single dashboard UI served from :8097 — same view for local, ngrok public, and admin.
 */
export function MaestroCasesPage() {
  useEffect(() => {
    document.title = "Maestro Case — PC Doctor | InnerChispa";
  }, []);

  return (
    <PageShell
      title="Maestro Case — PC Doctor"
      subtitle="InnerChispa · shared dashboard (local + public + jury)"
    >
      <iframe
        title="PC Doctor Maestro Dashboard"
        src="/uipath-copilot/dashboard"
        style={{
          width: "100%",
          height: "calc(100vh - 120px)",
          border: "none",
          borderRadius: 8,
          background: "#0b1120",
        }}
      />
    </PageShell>
  );
}
