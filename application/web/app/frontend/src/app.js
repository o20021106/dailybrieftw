import React from "react";
import ReactAudioPlayer from 'react-audio-player';
import Datetime from "react-datetime";
import moment from "moment";
import "react-datetime/css/react-datetime.css";
import 'bootstrap/dist/css/bootstrap.min.css';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Navbar from 'react-bootstrap/Navbar';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faGithub } from '@fortawesome/free-brands-svg-icons'
import { faEnvelope} from '@fortawesome/free-solid-svg-icons';

import style from './css/style.module.css'

import Articles from "./article_container";


class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      articles: [],
      audio_url: "",
    };
  }

  handelFetchedData(data) {
    console.log(data)
    if ("articles" in data && "audio_url" in data ) {
      this.setState({...this.state, articles: data["articles"],
                     audio_url: data["audio_url"]})
    }
  }

  fetchArticles(date = "") {
    var url = "https://dailybrieftw-jkrsedbirq-de.a.run.app//brief"
    
    if (date==""){
      var targetDate = new Date();
      targetDate.setDate(targetDate.getDate() - 1);

      var year = targetDate.getFullYear();
      var month = (targetDate.getMonth()+1);
      var day =  targetDate.getDate();
      date = year + '-' + (month<=9 ? '0' + month : month) + '-' + (day <= 9 ? '0' + day : day);
    }
    url = url + "?date=" + date
    fetch(url, {mode: 'cors'})
    .then(response => response.json())
    .then(this.handelFetchedData.bind(this));
  }

  handleDate(date) {
    console.log(date)
    console.log(date._d)
    date = moment(date).format("YYYY-MM-DD");
    console.log(date)
    this.fetchArticles(date)
  }

  isValidDate(currentDate) {
    const start = moment("2021-01-26").format('YYYY-MM-DD');
    const now = moment()
    return currentDate.isAfter(start) && now.isAfter(currentDate)
  }

  render() {
    return (
      <div className={style.container}>
        <Container className={style.content} fluid="md">
          <Row className="align-content-center">
            <Col>
              <h1 className={["text-center", style.title].join(" ")}>每日簡報</h1>
            </Col>
          </Row>
          <Row>
            <Col className="d-flex justify-content-center align-self-center" sm={6}>
              <div  className={style.gadget}>
                <Datetime onChange={this.handleDate.bind(this)}
                  initialValue={new Date()}
                  isValidDate={this.isValidDate}
                  dateFormat="YYYY-MM-DD"
                  timeFormat={false}
                />
              </div>
            </Col>
            <Col className="d-flex justify-content-center align-self-center" sm={6}> 
              <div className={style.gadget}>
                <ReactAudioPlayer
                  src={this.state.audio_url}
                  controls
                  className={style.audio_player}
                />
              </div>
            </Col>
          </Row>
          <div><Articles articles={this.state.articles}/></div>
        </Container>
        <Navbar bg="dark" variant="dark" fixed="bottom" className={style.footer_container}>
          <div className={style.footer}>
              <a className={["text-light", style.icon].join(" ")} href="https://github.com/o20021106/dailybrieftw">
                <FontAwesomeIcon icon={faGithub} size="lg" />
              </a>
              <a className={["text-light", style.icon].join(" ")} href="mailto: o20021106@gmail.com">
                <FontAwesomeIcon icon={faEnvelope} size="lg" />
              </a>
          </div>
        </Navbar>

      </div>
    );
  }
  componentDidMount() {
    this.fetchArticles();
  } 
}
 
export default App;
