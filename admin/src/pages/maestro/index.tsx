import { useCallback, useEffect, useState } from "react";
import { Button, Card, Space, Table, Tag, Typography, message } from "antd";
import { ReloadOutlined, ThunderboltOutlined } from "@ant-design/icons";
import { PageShell } from "../../components/PageShell";

type MaestroCase = {
  case_id: string;
  stage?: string;
  incident_type?: string;
  severity?: string;
  client_name?: string;
  needs_human?: boolean;
  updated_at?: string;
};

type StatusPayload = {
  uipath_maestro?: { configured?: boolean; reachable?: boolean; base_url?: string };
  public_base_url?: string;
};

export function MaestroCasesPage() {
  const [cases, setCases] = useState<MaestroCase[]>([]);
  const [status, setStatus] = useState<StatusPayload | null>(null);
  const [loading, setLoading] = useState(false);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const [casesRes, statusRes] = await Promise.all([
        fetch("/uipath-copilot/api/v1/cases?limit=50"),
        fetch("/uipath-copilot/status"),
      ]);
      const casesJson = await casesRes.json();
      const statusJson = await statusRes.json();
      setCases(casesJson.cases || []);
      setStatus(statusJson);
    } catch {
      message.error("No se pudo conectar con uipath-copilot :8097");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  const triggerDemo = async () => {
    setLoading(true);
    try {
      const r = await fetch("/uipath-copilot/api/v1/demo/trigger-sample");
      const j = await r.json();
      if (!r.ok) throw new Error(j.detail || "Error demo");
      message.success(`Caso demo: ${j.case_id || "OK"}`);
      await load();
    } catch (e) {
      message.error(String(e));
    } finally {
      setLoading(false);
    }
  };

  const uip = status?.uipath_maestro;

  return (
    <PageShell title="Maestro Case — PC Doctor" subtitle="Backend :8097 · datos reales MongoDB">
      <Space direction="vertical" size="large" style={{ width: "100%" }}>
        <Card size="small">
          <Space wrap>
            <Tag color={uip?.reachable ? "green" : uip?.configured ? "orange" : "default"}>
              UiPath OAuth: {uip?.reachable ? "conectado" : uip?.configured ? "configurado (error)" : "pendiente .env"}
            </Tag>
            <Tag>Webhook: {status?.public_base_url || "—"}/api/v1/uipath-webhook</Tag>
            <Button icon={<ReloadOutlined />} onClick={load} loading={loading}>
              Actualizar
            </Button>
            <Button type="primary" icon={<ThunderboltOutlined />} onClick={triggerDemo} loading={loading}>
              Demo real (MongoDB)
            </Button>
          </Space>
        </Card>

        <Table
          rowKey="case_id"
          loading={loading}
          dataSource={cases}
          pagination={{ pageSize: 10 }}
          columns={[
            { title: "Caso", dataIndex: "case_id", ellipsis: true },
            { title: "Cliente", dataIndex: "client_name" },
            { title: "Incidente", dataIndex: "incident_type" },
            { title: "Severidad", dataIndex: "severity" },
            { title: "Etapa", dataIndex: "stage" },
            {
              title: "HITL",
              dataIndex: "needs_human",
              render: (v: boolean) => (v ? <Tag color="red">Sí</Tag> : <Tag>No</Tag>),
            },
          ]}
        />

        <Typography.Paragraph type="secondary">
          Documentación en MongoDB: <code>GET /uipath-copilot/api/v1/project-docs</code>
        </Typography.Paragraph>
      </Space>
    </PageShell>
  );
}
