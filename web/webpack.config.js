const webpack = require('webpack');
const { resolve } = require('path');

module.exports = {
    entry: [
        'react-hot-loader/patch',
        'webpack-dev-server/client?http://localhost:8080 --hot --inline',
        'webpack/hot/only-dev-server',
        './main.jsx'
    ],
    output: {
        filename: 'bundle.js',
        path: resolve(__dirname, 'static'),
        publicPath: ''
    },

    devServer: {
        hot: true,
        contentBase: resolve(__dirname, 'static')
    },

    module: {
        rules: [
            {
                test: /\.js$/,
                loaders: [
                    'babel-loader'
                ],
                exclude: /node_modules/
            },
            {
                test: /\.scss$/,
                exclude: /node_modules/,
            },
            {
                test: /\.jsx?$/,
                loader: 'babel-loader',
                exclude: /node_modules/,
                query: {
                    plugins: [
                        'babel-plugin-transform-react-jsx'
                    ]
                }
            }
        ]
    },

    plugins: [
        new webpack.HotModuleReplacementPlugin()
    ],

    resolve: {
        extensions: ['.js', '.jsx']
    }
};