import mongoose from 'mongoose';
import Game from '../models/gameModel';

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  try {
    // Connect to MongoDB if not already connected
    if (mongoose.connections[0].readyState !== 1) {
      await mongoose.connect(process.env.MONGODB_URI, {
        useNewUrlParser: true,
        useUnifiedTopology: true,
      });
    }

    // Log received data
    console.log('Received body:', req.body);

    // Create new game document using the data directly
    const newGame = new Game(req.body);

    // Validate the document
    await newGame.validate();

    // Save the game data
    const savedGame = await newGame.save();

    return res.status(200).json({
      success: true,
      message: 'Game data saved successfully',
      data: savedGame
    });

  } catch (error) {
    console.error('Error details:', {
      message: error.message,
      stack: error.stack,
      name: error.name
    });
    
    // If it's a validation error, send more specific error message
    if (error.name === 'ValidationError') {
      return res.status(400).json({
        error: 'Validation failed',
        details: Object.values(error.errors).map(err => err.message)
      });
    }

    return res.status(500).json({
      error: 'Failed to save game data',
      details: error.message || error
    });
  }
}