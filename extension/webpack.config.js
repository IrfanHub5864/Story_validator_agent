// webpack.config.js - SIMPLE VERSION (NO CERTIFICATES)
const path = require('path');

module.exports = {
    mode: 'development',
    entry: './src/work-item-review.js',
    output: {
        filename: 'bundle.js',
        path: path.resolve(__dirname, 'dist'),
    },
    devServer: {
        static: {
            directory: path.join(__dirname, 'src'),
        },
        port: 3000,
        hot: true,
        open: true
    }
};