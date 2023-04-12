import React from 'react';
import { Row, Col, Button, Form } from 'react-bootstrap';
import '../css/SearchResultPage.css';
import { Search } from 'react-bootstrap-icons';

function SearchForm({ setLocation, setSearchData }) {
    const [startLocation, setStartLocation] = React.useState("");
    const [endLocation, setEndLocation] = React.useState("");

    const handleSearch = () => {
        fetch("https://test-vedhika.d186pebvqnkz8n.amplifyapp.com/search/", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "startLocation": startLocation,
                "endLocation": endLocation,
            })
        }).then((res) => res.json()
            .then((result) => {
                setLocation(
                    startLocation,
                    endLocation,
                    result['pickupLat'],
                    result['pickupLng'],
                    result['dropoffLat'],
                    result['dropoffLng']);
                setSearchData(result)
            })
        );
    }

    return (
        <Form>
            <Row>
                <Col>
                    <Form.Group className="mb-3" controlId="formStartLocation">
                        <Form.Label>Start Location</Form.Label>
                        <Form.Control type="text" placeholder="Enter starting location" onChange={(event) => setStartLocation(event.target.value)} />
                        <Form.Text className="text-muted">
                            We'll never share your information with anyone else.
                        </Form.Text>
                    </Form.Group>
                </Col>
                <Col>
                    <Form.Group className="mb-3" controlId="formdestination">
                        <Form.Label>Destination</Form.Label>
                        <Form.Control type="text" placeholder="Enter destination" onChange={(event) => setEndLocation(event.target.value)} />
                    </Form.Group>
                </Col>
                <Col className="search-form-submit-button">
                    <Button variant="primary" type="submit" onClick={(event) => {
                        event.preventDefault();
                        handleSearch();
                    }}>
                        <Search className="icon-margin" />  Search
                    </Button>
                </Col>
            </Row>
        </Form>
    );
}

export default SearchForm;