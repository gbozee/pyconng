import path from 'path';
import webpack from 'webpack';
import ForceCaseSensitivityPlugin from 'force-case-sensitivity-webpack-plugin';
import BundleTracker from 'webpack-bundle-tracker';

module.exports = () => {
  const NODE_ENV = process.env.NODE_ENV;
  let plugins = [
    // add all common plugins here
    new webpack.DefinePlugin({
      'process.env': {
        NODE_ENV: JSON.stringify(NODE_ENV),
      },
    }),
    // Promise and fetch polyfills
    new webpack.ProvidePlugin({
    //   Promise: 'imports?this=>global!exports?global.Promise!es6-promise',
    //   fetch: 'imports?this=>global!exports?global.fetch!whatwg-fetch',
      $: 'jquery',
      jQuery: 'jquery',
      'windows.jQuery': 'jquery',
    }),
    new BundleTracker({filename: './webpack-stats.json'}),
    new ForceCaseSensitivityPlugin(),  // OSX wont check but other unix os will
    new webpack.NoErrorsPlugin(),
  ];
  if (NODE_ENV !== 'test') {
    // karma webpack can't use these
    plugins = [
      ...plugins,
      // vendor chuncks
    //   new webpack.optimize.CommonsChunkPlugin({
    //     name: 'vendor',
    //     minChunks: Infinity,
    //     filename: 'vendor-[hash].js',
    //   }),
    //   // shared stuff between chuncks
    //   new webpack.optimize.CommonsChunkPlugin({
    //     name: 'common',
    //     filename: 'common-[hash].js',
    //     chunks: [],  // add common modules here
    //   }),
    ];
  }

  return {
    devtool: 'inline-source-map',
    entry: './src/main.js',
    output: {
      path: __dirname + '/static/js',
      publicPath: 'http://localhost:8080/bundles/',
      filename: 'bundle.js',
    },
    plugins,
    module: {
      loaders: [
        {
          test: /\.jsx?$/,
          exclude: /node_modules/,
          loaders: ['babel-loader'],
        },
    // {test: /\.scss$/, loader: 'style-loader!css-loader!sass-loader'},
    // {test: /\.css$/, loader: 'style-loader!css-loader'},
    // {test: /\.(png|jpg|gif)$/, loader: 'url-loader', query: {limit: 8192}},  // inline base64 URLs <=8k
    // {test: /\.(ttf|eot|svg)(\?v=[0-9]\.[0-9]\.[0-9])?$/, loader: 'file-loader'},
      ], // add all common loaders here
    },
    resolve: {
      extensions: ['', '.js', '.jsx'],
      modules: [
        'node_modules',
        'bower_components',
      ],
    },
    externals: {
      'jquery': 'jQuery',
    },

  };
};
