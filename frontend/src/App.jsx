import { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Calculator,
  Utensils,
  Newspaper,
  Terminal,
  ExternalLink,
  X,
  Send,
  AlertCircle,
  Loader2,
} from "lucide-react";
import ReactMarkdown from "react-markdown";
import axios from "axios";
import projectsData from "./projects.json";
import "./index.css";

const IconMap = {
  Calculator,
  Utensils,
  Newspaper,
};

function App() {
  const [selectedProject, setSelectedProject] = useState(null);
  const [demoMode, setDemoMode] = useState(false);

  return (
    <div className="container">
      <header className="nav-header">
        <div>
          <h1 className="gradient-text" style={{ fontSize: "2.5rem" }}>
            AI Agent Workspace
          </h1>
          <p style={{ color: "var(--text-muted)", marginTop: "0.5rem" }}>
            Interactive dashboard for managing and testing autonomous agents.
          </p>
        </div>
        <div
          className="status-indicator"
          style={{
            display: "flex",
            alignItems: "center",
            gap: "0.5rem",
            color: "var(--success)",
          }}
        >
          <div
            style={{
              width: 8,
              height: 8,
              borderRadius: "50%",
              background: "currentColor",
              boxShadow: "0 0 10px currentColor",
            }}
          />
          <span style={{ fontSize: "0.85rem", fontWeight: 600 }}>
            System Online
          </span>
        </div>
      </header>

      <main className="grid-layout">
        {projectsData.map((project) => (
          <ProjectCard
            key={project.id}
            project={project}
            onSelect={() => {
              setSelectedProject(project);
              setDemoMode(true);
            }}
          />
        ))}
      </main>

      <AnimatePresence>
        {demoMode && selectedProject && (
          <DemoModal
            project={selectedProject}
            onClose={() => {
              setDemoMode(false);
              setSelectedProject(null);
            }}
          />
        )}
      </AnimatePresence>
    </div>
  );
}

function ProjectCard({ project, onSelect }) {
  const Icon = IconMap[project.icon] || Terminal;

  return (
    <motion.div
      className="card"
      whileHover={{ y: -5 }}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
    >
      <div style={{ padding: "1.5rem" }}>
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            marginBottom: "1rem",
          }}
        >
          <div
            style={{
              width: 48,
              height: 48,
              borderRadius: 12,
              background: "rgba(139, 92, 246, 0.1)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              color: "var(--primary)",
            }}
          >
            <Icon size={24} />
          </div>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="btn btn-secondary"
            onClick={onSelect}
            style={{ padding: "0.5rem 1rem", fontSize: "0.85rem" }}
          >
            {project.type === "app" ? "Launch App" : "Open Terminal"}
            {project.type === "app" ? (
              <ExternalLink size={14} />
            ) : (
              <Terminal size={14} />
            )}
          </motion.button>
        </div>

        <h3 style={{ fontSize: "1.25rem", marginBottom: "0.5rem" }}>
          {project.title}
        </h3>
        <p
          style={{
            color: "var(--text-muted)",
            fontSize: "0.95rem",
            lineHeight: 1.6,
            marginBottom: "1.5rem",
            minHeight: "3rem",
          }}
        >
          {project.description}
        </p>

        <div style={{ display: "flex", flexWrap: "wrap", gap: "0.5rem" }}>
          {project.tags.map((tag) => (
            <span key={tag} className="tag">
              {tag}
            </span>
          ))}
        </div>
      </div>
    </motion.div>
  );
}

function DemoModal({ project, onClose }) {
  const [input, setInput] = useState("");
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(false);
  const scrollRef = useRef(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [logs]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const cmd = input;
    setInput("");
    setLogs((prev) => [...prev, { type: "user", content: cmd }]);
    setLoading(true);

    try {
      if (project.id === "agent01") {
        const res = await axios.post(project.apiEndpoint, { query: cmd });
        setLogs((prev) => [...prev, { type: "system", content: res.data.response }]);
      } else if (project.id === "agent03") {
        const res = await axios.post(project.apiEndpoint, { topic: cmd });
        // Store final output + per-agent sections
        setLogs((prev) => [
          ...prev,
          {
            type: "agent-sections",
            finalOutput: res.data.final_output,
            tasks: res.data.tasks_output || [],
          },
        ]);
      }
    } catch (err) {
      setLogs((prev) => [
        ...prev,
        { type: "error", content: `Error: ${err.message}` },
      ]);
    } finally {
      setLoading(false);
    }
  };

  if (project.type === "app") {
    window.open(project.demoUrl, "_blank");
    onClose();
    return null;
  }

  return (
    <motion.div
      className="modal-overlay"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        background: "rgba(0,0,0,0.8)",
        backdropFilter: "blur(5px)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        zIndex: 50,
      }}
      onClick={(e) => e.target === e.currentTarget && onClose()}
    >
      <motion.div
        className="glass"
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 0.9, opacity: 0 }}
        style={{
          width: "90%",
          maxWidth: "800px",
          height: "80vh",
          borderRadius: "16px",
          display: "flex",
          flexDirection: "column",
          overflow: "hidden",
          border: "1px solid var(--border)",
        }}
      >
        <div
          style={{
            padding: "1rem 1.5rem",
            borderBottom: "1px solid var(--border)",
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            background: "var(--bg-card)",
          }}
        >
          <div
            style={{ display: "flex", alignItems: "center", gap: "0.75rem" }}
          >
            <Terminal size={20} style={{ color: "var(--primary)" }} />
            <h3 style={{ color: "white", margin: 0 }}>
              {project.title} Console
            </h3>
          </div>
          <button
            onClick={onClose}
            style={{
              background: "none",
              border: "none",
              color: "var(--text-muted)",
              cursor: "pointer",
            }}
          >
            <X size={24} />
          </button>
        </div>

        <div
          ref={scrollRef}
          className="terminal"
          style={{
            flex: 1,
            borderRadius: 0,
            border: "none",
            borderBottom: "1px solid var(--border)",
          }}
        >
          <div style={{ color: "var(--text-muted)", marginBottom: "1rem" }}>
            Welcome to {project.title} CLI v2.0
            <br />
            Connected to 127.0.0.1 via FastAPI
            <br />
            Type execution command to begin...
          </div>

          {logs.map((log, idx) => (
            <div key={idx} style={{ marginBottom: "0.75rem" }}>
              {log.type === "user" ? (
                <div style={{ color: "white", display: "flex", gap: "0.5rem" }}>
                  <span style={{ color: "var(--accent)" }}>❯</span>
                  {log.content}
                </div>
              ) : log.type === "error" ? (
                <div style={{ color: "var(--error)", display: "flex", gap: "0.5rem" }}>
                  <AlertCircle size={14} style={{ marginTop: 3 }} />
                  {log.content}
                </div>
              ) : log.type === "agent-sections" ? (
                <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
                  {/* Per-agent output sections */}
                  {log.tasks.map((task, tIdx) => (
                    <div
                      key={tIdx}
                      style={{
                        border: "1px solid rgba(139,92,246,0.3)",
                        borderRadius: "8px",
                        overflow: "hidden",
                      }}
                    >
                      <div
                        style={{
                          background: "rgba(139,92,246,0.15)",
                          padding: "0.4rem 0.75rem",
                          fontSize: "0.8rem",
                          fontWeight: 700,
                          color: "var(--primary)",
                          letterSpacing: "0.05em",
                          textTransform: "uppercase",
                        }}
                      >
                        🤖 {task.agent}
                      </div>
                      <div style={{ padding: "0.75rem", color: "#a7f3d0", lineHeight: 1.6 }}>
                        <ReactMarkdown>{task.output || "(no output)"}</ReactMarkdown>
                      </div>
                    </div>
                  ))}
                  {/* Final combined output */}
                  {log.tasks.length === 0 && (
                    <div style={{ color: "#a7f3d0", paddingLeft: "1.2rem", lineHeight: 1.5 }}>
                      <ReactMarkdown>{log.finalOutput || "(no output)"}</ReactMarkdown>
                    </div>
                  )}
                </div>
              ) : (
                <div style={{ color: "#a7f3d0", paddingLeft: "1.2rem", lineHeight: 1.5 }}>
                  <ReactMarkdown>
                    {typeof log.content === "string"
                      ? log.content
                      : JSON.stringify(log.content)}
                  </ReactMarkdown>
                </div>
              )}
            </div>
          ))}

          {loading && (
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: "0.5rem",
                color: "var(--text-muted)",
              }}
            >
              <Loader2
                size={16}
                className="animate-spin"
                style={{ animation: "spin 1s linear infinite" }}
              />
              <span>Processing agent workflow...</span>
            </div>
          )}
          <style>{`@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }`}</style>
        </div>

        <div style={{ padding: "1rem", background: "var(--bg-card)" }}>
          <form onSubmit={handleSubmit} className="input-group">
            <span
              style={{
                display: "flex",
                alignItems: "center",
                color: "var(--accent)",
                fontWeight: "bold",
              }}
            >
              $
            </span>
            <input
              autoFocus
              className="input-field"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder={
                project.id === "agent03"
                  ? "Enter research topic..."
                  : "Enter math problem..."
              }
              disabled={loading}
              style={{
                background: "transparent",
                border: "none",
                boxShadow: "none",
                padding: 0,
                height: "auto",
                borderRadius: 0,
                borderBottom: "2px solid transparent",
              }}
            />
            <button
              type="button"
              className="btn btn-primary"
              disabled={loading}
              onClick={handleSubmit}
              style={{ padding: "0.5rem 1rem", marginLeft: "auto" }}
            >
              {loading ? "Running..." : "Execute"} <Send size={16} />
            </button>
          </form>
        </div>
      </motion.div>
    </motion.div>
  );
}

export default App;
