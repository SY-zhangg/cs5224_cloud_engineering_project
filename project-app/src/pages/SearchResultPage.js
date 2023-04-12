import React from "react";
import { Container, Row, Col, Button, Alert } from 'react-bootstrap'
import '../css/SearchResultPage.css';
import SearchForm from '../components/searchForm';
import SearchResultList from "../components/SearchResultList";

function SearchResultPage() {
    const [startLocation, setStartLocation] = React.useState("");
    const [endLocation, setEndLocation] = React.useState("");
    const [pickupLat, setPickupLat] = React.useState("");
    const [pickupLng, setPickupLng] = React.useState("");
    const [dropoffLat, setDropoffLat] = React.useState("");
    const [dropoffLng, setDropoffLng] = React.useState("");
    const [shouldDisplayResult, setShouldDisplayResult] = React.useState(false);
    const [predictData, setPredictData] = React.useState("");
    const [searchData, setSearchData] = React.useState("");

    const setLocation = (s, e, l1, l2, l3, l4) => {
        setStartLocation(s);
        setEndLocation(e);
        setPickupLat(l1);
        setPickupLng(l2);
        setDropoffLat(l3);
        setDropoffLng(l4);
        setShouldDisplayResult(true);
    };

    const handlePredict = () => {
        fetch("https://test-vedhika.d186pebvqnkz8n.amplifyapp.com/predict/", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "l1": pickupLat,
                "l2": pickupLng,
                "l3": dropoffLat,
                "l4": dropoffLng,
            })
        }).then((res) => res.json()
            .then((result) => {
                setPredictData(result);
            })
        );
    }

    let searchResultList = <div></div>;
    let searchPredictionList = <div></div>;

    if (predictData !== "") {
        searchPredictionList = <div className='search-result-list'>
            <Row>
                <Col sm={8}>
                    <h5>Price Prediction for the next 5 - 10 minutes</h5>
                </Col >
            </Row>
            <Row>
                <SearchResultList data={predictData} />
            </Row>
        </div>
    }

    if (shouldDisplayResult) {
        if (startLocation.length === 0) {
            searchResultList = <Alert variant='danger'>
                Please enter start location.
            </Alert>
        } else if (endLocation.length === 0) {
            searchResultList = <Alert variant='danger'>
                Please enter end location.
            </Alert>
        }

        if (searchData !== "") {
            searchResultList = <div>
                <div className='search-result-list'>
                    <Row>
                        <Col sm={8}>
                            <h5>Search Result from {startLocation} to {endLocation}</h5>
                        </Col >
                    </Row>
                    <Row>
                        <SearchResultList data={searchData} />
                    </Row>
                    <br /><br />
                    <Button variant="outline-success" onClick={(event) => {
                        event.preventDefault();
                        handlePredict();
                    }}>Request for next window</Button>
                </div>
            </div >
        }

    }

    return (
        <Container>
            <div className='search-result'>
                <Row>
                    <Col sm={8}>
                        <h3>Search For the Cheapest Provider</h3>
                        <hr />
                    </Col >
                    <Col sm={4}><Button variant="outline-success">View Search History</Button></Col>
                </Row>
                <Row>
                    <SearchForm setLocation={setLocation} setSearchData={setSearchData} />
                </Row>
                {searchResultList}
                {searchPredictionList}
            </div>
        </Container>
    );
}

export default SearchResultPage;