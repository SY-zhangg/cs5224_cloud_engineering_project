import React from 'react';
import { Button, Row, Col, Container } from 'react-bootstrap';
import '../css/SearchResultPage.css';
import 'bootstrap/dist/css/bootstrap.min.css'
import grab from '../assets/grab.svg';
import uber from '../assets/uber.svg';

function SearchResultList({ data }) {
  const redirectToGrab = () => {
    window.open('https://www.grab.com/sg/');
  };
  const redirectToUber = () => {
    window.open('https://www.uber.com/');
  };

  const grabResultRow = <div className="border rounded search-result-list-item">
    <Row>
      <Col><img src={grab} className="grab-logo" alt="grab" /></Col>
      <Col><div className="search-result-list-item-text">$ 10 - 20 </div></Col>
      <Col><Button onClick={redirectToGrab}>Go To App</Button></Col>
    </Row>
  </div>;

  const uberResultRow = <div className="border rounded search-result-list-item">
    <Row>
      <Col><img src={uber} className="uber-logo" alt="grab" /></Col>
      <Col><div className="search-result-list-item-text">$ 10 - 20 </div></Col>
      <Col><Button onClick={redirectToUber}>Go To App</Button></Col>
    </Row>
  </div>;

  return (
    <Container>
      {grabResultRow}
      {uberResultRow}
    </Container>
  );
}

export default SearchResultList;