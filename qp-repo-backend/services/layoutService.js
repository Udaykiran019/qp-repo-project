const axios = require('axios');

const runLayoutDetection = async (documentId, pages) => {
    const { data } = await axios.post(`${process.env.PYTHON_SERVICE_URL}/detect-layout`, {
        documentId,
        pages
    });
    return data;
};

module.exports = { runLayoutDetection };