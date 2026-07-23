const express = require('express');
const router = express.Router();
const fs = require('fs');
const upload = require('../middlewares/upload');
const { runPreprocessing } = require('../services/preprocessingService');
const { runLayoutDetection } = require('../services/layoutService');
const { randomUUID } = require('crypto');

router.post('/upload', upload.single('paper'), async (req, res) => {
    if (!req.file) return res.status(400).json({ error: 'No file uploaded.' });

    try {
        const documentId = randomUUID();
        const preprocessResult = await runPreprocessing(req.file.path, documentId);
        const layoutResult = await runLayoutDetection(documentId, preprocessResult.pages);

        await fs.promises.unlink(req.file.path).catch(() => {});

        res.status(200).json({
            message: 'Preprocessing and layout detection complete.',
            documentId,
            pages: preprocessResult.pages,
            layout: layoutResult.layout
        });
    } catch (error) {
        const details = error.response?.data || error.message || 'Unknown error';
        console.error('Pipeline failed:', details);
        await fs.promises.unlink(req.file.path).catch(() => {});
        res.status(500).json({ error: 'Pipeline failed.', details });
    }
});

module.exports = router;