// api/get-game-data.js
const Game = require('../models/gameModels');

export default async function handler(req, res) {
  if (req.method === 'GET') {
    try {
      const games = await Game.find({});
      res.status(200).json(games);
    } catch (error) {
      console.error('Error fetching game data:', error);
      res.status(500).json({ error: 'Failed to fetch game data' });
    }
  } else {
    res.status(405).json({ error: 'Method Not Allowed' });
  }
}