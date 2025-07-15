import express from "express";
import fetch from "node-fetch";
import dotenv from "dotenv";

dotenv.config();

const app = express();
const PORT = process.env.PORT || 4000;
const GITEA_API = process.env.GITEA_API;
const TOKEN = process.env.GITEA_TOKEN;

if (!TOKEN || !GITEA_API) {
  console.error("❌ Erreur : TOKEN ou GITEA_API manquant dans .env");
  process.exit(1);
}

// Middleware CORS
app.use((req, res, next) => {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization");
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, PATCH");
  next();
});

// Proxy route
app.use("/api/git/*", async (req, res) => {
  const apiPath = req.originalUrl.replace("/api/git", "");
  const url = `${GITEA_API}${apiPath}`;

  try {
    const method = req.method;
    const headers = {
      "Content-Type": "application/json",
      Authorization: `token ${TOKEN}`,
    };

    const body = ["POST", "PUT", "PATCH"].includes(method)
      ? JSON.stringify(req.body)
      : undefined;

    const response = await fetch(url, { method, headers, body });
    const data = await response.json();

    res.status(response.status).json(data);
  } catch (err) {
    console.error("Erreur proxy :", err);
    res.status(500).json({ error: "Erreur proxy Gitea" });
  }
});

app.listen(PORT, () => {
  console.log(`✅ Proxy Gitea lancé sur http://localhost:${PORT}`);
});
