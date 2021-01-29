import React from "react";
import 'bootstrap/dist/css/bootstrap.min.css';
import Card from 'react-bootstrap/Card';
import Badge from 'react-bootstrap/Badge';
import style from './css/style.module.css'

class Article extends React.Component {
  render() {
    return (
    <div className={style.article}>
      <Card>
        <Card.Img variant="top"/>
        <Card.Body>
            <Card.Title>{this.props.articleData["title"]}</Card.Title>
            <Card.Text>{this.props.articleData["content"]}</Card.Text>
            <Badge variant="secondary">來源：{this.props.articleData["source"]}</Badge>
        </Card.Body>
      </Card>
    </div>
    );
  }
}
 
export default Article;
