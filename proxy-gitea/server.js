import express from "express";
import dotenv from "dotenv";
import axios from 'axios';

dotenv.config();

const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());

// Endpoint pour obtenir un token d'accès
app.get('/auth/token', async (req, res) => {
  try {
    const response = await axios.post(
      `${process.env.GITEA_API_URL}/oauth2/access_token`,
      new URLSearchParams({
        client_id: process.env.GITEA_CLIENT_ID,
        client_secret: process.env.GITEA_CLIENT_SECRET,
        code: req.query.code,
        redirect_uri: `${process.env.GITEA_SITE_DOMAIN}/callback`,
        grant_type: 'authorization_code'
      }),
      {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      }
    );
    res.json(response.data);
  } catch (error) {
    console.error('Error fetching access token:', error);
    res.status(500).json({ error: 'Failed to fetch access token' });
  }
});

app.listen(port, () => {
  console.log(`Proxy server running on port ${port}`);
});
