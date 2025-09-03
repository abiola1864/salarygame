require('dotenv').config();
const express = require('express');
const mongoose = require('mongoose');
const path = require('path');
const cors = require('cors');
const gameRoutes = require('./routes/gameRoutes');

const app = express();
const PORT = process.env.PORT || 3040;

// ---------- Middleware ----------
app.use(express.json({ limit: '10mb' })); // Handle JSON with size limit
app.use(express.urlencoded({ extended: true }));

// CORS setup
app.use(
  cors({
    origin: [
      process.env.FRONTEND_URL || 'http://localhost:3000',
      'http://localhost:3040',
    ],
    methods: ['GET', 'POST', 'PUT', 'DELETE'],
    allowedHeaders: ['Content-Type', 'Authorization'],
    credentials: true,
  })
);

// Security headers
app.use((req, res, next) => {
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('X-XSS-Protection', '1; mode=block');
  next();
});

// ---------- Database Connection ----------
const connectWithRetry = () => {
  const mongoURI = process.env.MONGODB_URI;

  if (!mongoURI) {
    console.error('❌ MongoDB connection string is missing. Exiting...');
    process.exit(1);
  }

  mongoose
    .connect(mongoURI, { serverSelectionTimeoutMS: 5000 })
    .then(() => console.log('✅ MongoDB connected successfully'))
    .catch((err) => {
      console.error('❌ MongoDB connection error:', err.message);
      console.log('Retrying in 5 seconds...');
      setTimeout(connectWithRetry, 5000);
    });
};

connectWithRetry();

mongoose.connection.on('error', (err) =>
  console.error('❌ MongoDB runtime error:', err.message)
);

mongoose.connection.on('disconnected', () => {
  console.warn('⚠️ MongoDB disconnected. Reconnecting...');
  connectWithRetry();
});

// ---------- Routes ----------
app.use('/api', gameRoutes);

// Serve static files (templates folder)
app.use(express.static(path.join(__dirname, 'templates')));

// ---------- Error Handling ----------
app.use((err, req, res, next) => {
  console.error('🔥 Error:', err.stack);
  res.status(err.status || 500).json({
    error: {
      message:
        process.env.NODE_ENV === 'production'
          ? 'Internal server error'
          : err.message,
      status: err.status || 500,
    },
  });
});

// Handle 404s
app.use((req, res) =>
  res.status(404).json({ error: { message: 'Not found', status: 404 } })
);

// ---------- Start Server ----------
const server = app.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`);
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('🛑 SIGTERM received. Shutting down...');
  server.close(() => {
    mongoose.connection.close(false, () => {
      console.log('✅ MongoDB connection closed.');
      process.exit(0);
    });
  });
});

module.exports = app;
