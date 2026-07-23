const axios = require('axios');

const runPreprocessing = async (filePath, documentId) => {
    const { data } = await axios.post(`${process.env.PYTHON_SERVICE_URL}/preprocess`, {
        filePath,
        documentId
    });
    return data; // { documentId, pages: [{page_number, type, image_path, dpi}, ...] }
};

module.exports = { runPreprocessing };