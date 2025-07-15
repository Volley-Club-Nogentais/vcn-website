import express from "express";
import fetch from "node-fetch";
import dotenv from "dotenv";
import cookieParser from "cookie-parser";

dotenv.config();
const app = express();

const PORT = process.env.PORT || 4000;
const {
  GITEA_API,
  GITEA_DOMAIN,
  GITEA_CLIENT_ID,
  GITEA_CLIENT_SECRET,
  GITEA_REDIRECT_URI,
} = process.env;

app.use(express.json());
app.use(cookieParser());

// CORS pour le frontend local
app.use((req, res, next) => {
  res.setHeader("Access-Control-Allow-Origin", "http://localhost:1313");
  res.setHeader("Access-Control-Allow-Credentials", "true");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization");
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE");
  next();
});

// Auth: redirection vers Gitea
app.get("/auth/login", (req, res) => {
  const redirect = `${GITEA_DOMAIN}/login/oauth/authorize?client_id=${GITEA_CLIENT_ID}&redirect_uri=${encodeURIComponent(GITEA_REDIRECT_URI)}&response_type=code`;
  res.redirect(redirect);
});

// Auth: callback de Gitea
app.get("/auth/callback", async (req, res) => {
  const code = req.query.code;

  console.log("OAuth2 payload:", {
      client_id: GITEA_CLIENT_ID,
      client_secret: GITEA_CLIENT_SECRET,
      code,
      redirect_uri: GITEA_REDIRECT_URI,
    });

  try {
    const tokenRes = await fetch(`${GITEA_DOMAIN}/login/oauth/access_token`, {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify({
        client_id: GITEA_CLIENT_ID,
        client_secret: GITEA_CLIENT_SECRET,
        code,
        redirect_uri: GITEA_REDIRECT_URI,
        grant_type: "authorization_code",
      }),
    });

    const tokenData = await tokenRes.json();
    if (tokenData.error) throw new Error(tokenData.error_description || "Erreur OAuth");

    const accessToken = tokenData.access_token;
    res.cookie("access_token", accessToken, { httpOnly: true, sameSite: "Lax" });
    res.redirect("http://localhost:1313/admin/");
  } catch (err) {
    console.error("OAuth2 error:", err);
    res.status(500).send("Erreur d’authentification");
  }
});

// API proxy (utilise le token stocké en cookie)
app.use("/api/git/*", async (req, res) => {
  const apiPath = req.originalUrl.replace("/api/git", "");
  const token = req.cookies.access_token;

  if (!token) return res.status(401).json({ error: "Non authentifié" });

  try {
    const response = await fetch(`${GITEA_API}${apiPath}`, {
      method: req.method,
      headers: {
        "Content-Type": "application/json",
        Authorization: `token ${token}`,
      },
      body: ["POST", "PUT", "PATCH"].includes(req.method) ? JSON.stringify(req.body) : undefined,
    });

    const data = await response.json();
    res.status(response.status).json(data);
  } catch (err) {
    console.error("Erreur proxy Gitea:", err);
    res.status(500).json({ error: "Erreur proxy Gitea" });
  }
});

app.listen(PORT, () => {
  console.log(`✅ Proxy OAuth2 Gitea lancé sur http://localhost:${PORT}`);
});
