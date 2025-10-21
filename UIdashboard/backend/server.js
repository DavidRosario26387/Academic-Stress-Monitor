const express = require('express');
const cors = require('cors');
const mongoose = require('mongoose');
require('dotenv').config();

const app = express();
const port = process.env.PORT || 5000;;

app.use(cors());
app.use(express.json());

// MongoDB connection
mongoose.connect('mongodb+srv://davidrosario_db_user:fdKIL0ZcLkSS3G1J@stresslogs.qq4rjja.mongodb.net/Hackathon?retryWrites=true&w=majority', { useNewUrlParser: true, useUnifiedTopology: true })
    .then(() => console.log('MongoDB connected'))
    .catch(err => console.error(err));

const StressLogSchema = new mongoose.Schema({
    Username: String,
    Time_stamp: Date,
    Message: String,
    Stress_label: String,
    Stress_category: String,
    Stress_Score: Number,
    Recommendation_given: String,
    Stress_Reason: String
});

// Third argument is collection name
const StressLog = mongoose.model('StressLog', StressLogSchema, 'Stress_logs');


// API routes
app.get('/api/logs', async (req, res) => {
    try {
        const logs = await StressLog.find({});
        res.json(logs);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

app.listen(port, () => console.log(`Server running on port ${port}`));
