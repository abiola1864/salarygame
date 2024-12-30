// api/fetch-game-data.js
const mongoose = require('mongoose');
const Game = require('../models/gameModel');
require('dotenv').config();

async function handler(req, res) {
    if (req.method !== 'GET') {
        return res.status(405).json({ error: 'Method Not Allowed' });
    }

    try {
        const gameData = await Game.find({})
            .sort({ stageName: 1, is_post_shock: 1 });

        return res.status(200).json({
            success: true,
            data: gameData
        });

    } catch (error) {
        console.error('Error fetching game data:', error);
        return res.status(500).json({
            success: false,
            error: 'Failed to fetch game data',
            details: error.message
        });
    }
}

module.exports = handler;