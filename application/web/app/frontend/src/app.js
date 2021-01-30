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
import Alert from 'react-bootstrap/Alert';
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
      showAlert: false,
      alertMessage: ""
    };
    this.fetchArticles = this.fetchArticles.bind(this);
    this.handelFetchedData = this.handelFetchedData.bind(this);
    this.handleDate = this.handleDate.bind(this);
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
    var now = new Date()
    var year = now.getFullYear();
    var month = (now.getMonth()+1);
    var day = now.getDate();
    var now_date = year + '-' + (month<=9 ? '0' + month : month) + '-' + (day <= 9 ? '0' + day : day);
    if (date==""){
      date = now_date
    }

    if (date == now_date && now.getHours() <= 15){
      this.setState({
        ...this.state,
        showAlert: true,
        alertMessage: "今天的簡報要到早上八點才會送出，請聽取其他日期簡報。"})
      console.log('show alert')
    }
    else {
      this.setState({
        ...this.state,
        showAlert: false,
        alertMessage: ""})
      url = url + "?date=" + date
      fetch(url, {mode: 'cors'})
      .then(response => response.json())
      .then(this.handelFetchedData);
    }
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
    const alertStyle = {
      visibility: this.state.showAlert ? "visible" : "hidden",
      display: this.state.showAlert ? "block" : "none",
      margin: "auto"
    };
    const articlesStyle = {
      visibility: this.state.showAlert ? "hidden" : "visible",
      display: this.state.showAlert ? "none" : "block",
      margin: "auto",
      padding: "10px 0px 30px 0px"
    };
    return (
      <div className={style.container}>
        <Container className={style.content} fluid="md">
          <Row className="align-content-center" style={{margin: "auto"}}>
            <Col>
              <h1 className={["text-center", style.title].join(" ")}>每日簡報</h1>
            </Col>
          </Row>
          <Row style={{margin: "auto"}}>
            <Col className="d-flex justify-content-center align-self-center" sm={6}>
              <div className={style.gadget}>
                <Datetime onChange={this.handleDate}
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
          <Row style={alertStyle} >
              <Alert variant="secondary">{this.state.alertMessage}</Alert>
          </Row>
          <Row style={articlesStyle}>
                <Articles articles={this.state.articles}/>
          </Row>
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
