// api/clear-game-data.js
const Game = require('../models/gameModels');

export default async function handler(req, res) {
  if (req.method === 'DELETE') {
    try {
      await Game.deleteMany({});
      res.status(200).json({ message: 'All game data cleared successfully' });
    } catch (error) {
      console.error('Error clearing game data:', error);
      res.status(500).json({ error: 'Failed to clear game data' });
    }
  } else {
    res.status(405).json({ error: 'Method Not Allowed' });
  }
}