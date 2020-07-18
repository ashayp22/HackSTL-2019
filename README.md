# GrinAI

![Preview](https://ashayp.com/images/projects/grinai.PNG)

### Project Details

GrinAI is a full deep learning pipeline that classifies grins on a face. This model is implemented in a Twitter Bot, which tweets jokes if a person is not grinning, and a realtime camera, which can be run locally and notifies the user if they are not grinning. 

### Hackathon

This project was submitted to HackSTL 2019 in August 2019, which was a hackathon hosted at the Schamburg Township Library for 2 days or 21 hours.

## Links

* [Check out the site in action](https://health-desk.herokuapp.com/)
* [Watch the demonstration video](https://youtu.be/EqEYL4vCNPE)
* [See the project submission on Devpost](https://devpost.com/software/healthdesk-mfj2hr)

## Technologies

* Python
* Node.js
* Keras
* OpenCV

## How We Built It

In order to develop the AI component, we chose to use Python and Keras. First, we found a public dataset of labeled mouths from a University. After applying preprocessing, we trained a Convolutional Neural Network to classify grins on the dataset. We experimented with different architectures and hyperparameters until we found a network with an accuracy of 91%. After this, we used this model and a Haar Cascade in a program that takes input from a computer camera and detects grins in real-time. In this program, the user has access to accuracy percentages and other controls.

Taking this one step further, we created a Twitter Bot using Node.js. After a user tweets a picture of themself, the picture is pulled from Twitter using the Twitter API and processed by our server. After the server recognizes a grin or no grin, the server tweets a response. If the person was grinning, then the server sends a message that says stay grinning. Otherwise, the server pulls jokes from a Joke API and tweets a random joke.

Overall, we were able to prove the concept of using Deep Learning and a Convolutional Neural Network to recognize grins. In addition, we implemented this concept in two unique ways.

## Authors

* [Ashay Parikh](https://www.linkedin.com/in/ashay-parikh-a0621619a/)
* [Skyler Gao](https://www.linkedin.com/in/skyler-gao-9683b01b2/)

## Contributing
We encourage people to contribute to our website and suggest changes. Please create a pull request and email [us](mailto:ashayp22@gmail.com) with your suggestion. 

For major changes, please open an issue first to discuss what you would like to change.

## License
[GNU General Public License v3.0](https://github.com/ashayp22/HackSTL-2019/blob/master/LICENSE)


