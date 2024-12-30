
//models/gameModels.js
const mongoose = require('mongoose');

const optionSchema = new mongoose.Schema({
    total: { type: Number, required: true, default: 0 },
    options: { type: Object, required: true, default: {} }
}, { _id: false }); 

const allocatedOptionsSchema = new mongoose.Schema({
    essentials: { type: optionSchema, required: true, default: () => ({ total: 0, options: {} }) },
    transport: { type: optionSchema, required: true, default: () => ({ total: 0, options: {} }) },
    lifestyle: { type: optionSchema, required: true, default: () => ({ total: 0, options: {} }) },
    savings: { type: optionSchema, required: true, default: () => ({ total: 0, options: {} }) }
}, { _id: false });

const gameSchema = new mongoose.Schema({
    stageName: { type: String, required: true, default: 'defaultStage' },
    date: { type: String, required: true, default: 'defaultDate' },
    time: { type: String, required: true, default: 'defaultTime' },
    user_id: { type: String, required: true, default: 'defaultUser' },
    total_amount: { type: Number, required: true, default: 0 },
    shock_amount: { type: Number, required: true, default: 0 },
    total_earning: { type: Number, required: true, default: 0 },
    specific_option: { type: String, required: true, default: 'defaultOption' },
    speed_bonus: { type: Number, required: true, default: 0 },
    pre_shock_earnings: { type: Number, required: true, default: 0 },
    amount_allocated_options: { type: allocatedOptionsSchema, required: true, default: () => ({}) },
    is_post_shock: { type: Boolean, required: true, default: false } // New field to track shock state
});

const Game = mongoose.model('Game', gameSchema);

module.exports = Game;