const path = require('path');

module.exports = {
    mode: 'development',
    entry: './auctions/static/App.js',
    output: {
        path: path.resolve(__dirname, 'auctions/static/'),
        filename: 'bundle.js'
    },
    module: {
        rules: [
            {
                test: /\.(js|jsx)$/,
                exclude: /node_modules/,
                use: ['babel-loader']
            },
            {
                test: /\.css$/,
                use: ['style-loader', 'css-loader']
            },
            {
                test: /\.(png|jpe?g|gif)$/i,
                use: ['file-loader']
            }
        ]
    }
};
