// routes/gameRoutes.js
const express = require('express');
const router = express.Router();
const Game = require('../models/gameModel');  // Make sure this path matches your file structure

// Save game data
router.post('/save-game-data', async (req, res) => {
  try {
    const gameData = req.body;
    const newGame = await Game.create(gameData);  // Using create instead of new Game()
    
    res.status(201).json({ 
      success: true, 
      message: 'Game data saved successfully', 
      data: newGame 
    });
  } catch (error) {
    console.error('Error saving game data:', error);
    res.status(500).json({ 
      success: false, 
      message: 'Error saving game data', 
      error: error.message 
    });
  }
});

// Get all game data
router.get('/get-game-data', async (req, res) => {
  try {
    const games = await Game.find();
    res.status(200).json({ success: true, data: games });
  } catch (error) {
    console.error('Error retrieving game data:', error);
    res.status(500).json({ 
      success: false, 
      message: 'Error retrieving game data', 
      error: error.message 
    });
  }
});

// Clear all game data
router.post('/clear-game-data', async (req, res) => {
  try {
    await Game.deleteMany({});
    res.status(200).json({ success: true, message: 'All game data cleared' });
  } catch (error) {
    console.error('Error clearing game data:', error);
    res.status(500).json({ 
      success: false, 
      message: 'Error clearing game data', 
      error: error.message 
    });
  }
});

router.get('/fetch-game-data', async (req, res) => {
  try {
      const games = await Game.find();
      res.status(200).json({ success: true, data: games });
  } catch (error) {
      console.error('Error retrieving game data:', error);
      res.status(500).json({ 
          success: false, 
          message: 'Error retrieving game data', 
          error: error.message 
      });
  }
});


module.exports = router;