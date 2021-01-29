import React from "react";
import Article from "./article"

class ArticleContainer extends React.Component {
  render() {
    return (
      <div>
        {this.props.articles.map((el, index) => (
          <Article key={index} articleData={el} />
        ))}
      </div>
    );
  }
}


export default ArticleContainer;
