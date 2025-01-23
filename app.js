jsx
import React, { useState } from "react";
import axios from "axios";
import { TextField, Button, List, ListItem, Typography } from "@mui/material";

const App = () => {
  const [query, setQuery] = useState("");
  const [responses, setResponses] = useState([]);

  const handleQuery = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/summarize/`, {
        params: { product_id: query },
      });
      setResponses([...responses, response.data]);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <Typography variant="h4">AI Chatbot</Typography>
      <TextField
        label="Enter Query"
        variant="outlined"
        fullWidth
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        style={{ marginBottom: "10px" }}
      />
      <Button variant="contained" onClick={handleQuery}>
        Submit
      </Button>
      <List>
        {responses.map((res, index) => (
          <ListItem key={index}>{JSON.stringify(res)}</ListItem>
        ))}
      </List>
    </div>
  );
};

export default App;