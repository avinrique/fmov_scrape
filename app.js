const express = require('express');
const { exec } = require('child_process');
const path = require('path');
const bodyParser = require('body-parser');

const app = express();
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));
app.use(express.static(path.join(__dirname, 'public')));
app.use(bodyParser.urlencoded({ extended: true }));

app.get('/', (req, res) => {
    res.render('index', { movies: [] });
});

app.post('/search', (req, res) => {



    const searchQuery = req.body.searchQuery;
    exec(`python app.py "${searchQuery}"`, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error executing script: ${error}`);
            res.status(500).send('Error searching movies');
            return;
        }
        if (stderr) {
            console.error(`Script stderr: ${stderr}`);
            res.status(500).send('Error searching movies');
            return;
        }
        try {
            movies = JSON.parse(stdout);
            res.render('index', { movies });
        } catch (parseError) {
            console.error(`Error parsing JSON: ${parseError}`);
            res.status(500).send('Error processing movie data');
        }
    });
});

app.listen(3001, () => {
    console.log('Server is running on http://localhost:3000');
});
