import React from 'react';
import ReactDOM from 'react-dom';

import App from './app';

const title = 'React with Webpack and Babel';
 
ReactDOM.render(
  <App />,
  document.getElementById('app')
);

module.hot.accept()
