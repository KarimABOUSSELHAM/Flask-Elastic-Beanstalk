# Flask-Elastic-Beanstalk

This project aims to build a Falsk application which is continuously deployed uising AWS Beanstalk. It is the result of forking the project referrenced [here](https://https://github.com/noahgift/Flask-Elastic-Beanstalk)

The original project requires the usage of AWS Cloud9, but this is no longer possible for free tier users like me at the time of writing these lines. Therefore, I chose to clone the github repository once forked via the `git clone <repository url`, then in my VS Code I opened the terminal and changed the directory to the location where the repository was cloned.

Of course you have to install the makefile extension your vs code if you don't have it, as we will need to use make commands in the terminal for the current project.

A possible question can arise before we start building the project is whether it is possible to use the `eb cli` in your vs code. And the is answer is Yes, you can absolutely install it via the `awsebcli` dependency. In this project this task will be assured through the `make install` command defined in the makefile.

Now that you have set up the project requirements and you have changed your current directory in VS Code terminal to the cloned repository let's start working.
Note that I am using here extensively my VS Code installed on a windows 11 OS, 64 bits. Therefore all the system commands will be written in pre installed powershell (version 5). If you are interested you may contribute to this small project by adding bash commands for other OS.


### Deploy via VS Code + AWS Code Build


*You can refer to tutorial [here as well for Flask EB](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-flask.html)*

  **1.** Delete the .elasticbeanstalk directory either using the VS Code terminal command `rmdir /s /q .elasticbeanstalk` or doing it manually from your desktop.
At this stage it is also recommendable to check that automatic sync is disabled in order for the github repository not to automatically restore the intial state obtained after fork.

  **2.** Create a python virtual environment, activate it and run the `make all` command which helps installing the required dependencies, linting the code scripts and testing the code.
Note at this stage the use of pystest as a testing framework and the absence of a python script to test the code contained in `application.py` script. This means you have to create a test file in the project directory named `test_application`.

You can see the `test_application` file to have an idea of the chosen tests in this case.
Now to sum up here are the commands you need to execute in sequence:

`python -m venv ~/.eb`
`.\~/.eb/Scripts/Activate`
`make all`

  **3.** Now it is time to replace the removed .elasticbeanstalk directory and initialize a new elastic beanstalk app which we'll call `flask-continuous-delivery`. Here's how you can do it:

`eb init -p python-3.7 flask-continuous-delivery --region us-east-1`
Of course if you didn't setup a IAM user group you have to, beacause you will prompted to enter your access_key_ID and secret_access_key.

  **4.** Create remote elastic beanstalk instance in your VS Code terminal using the following command:

`eb create flask-continuous-delivery-env`
Here we called the instance `flask-continuous-delivery-env`. You can now check that this instance has been created as an EC2 environment from the AWS console.

  **5.**  Upload the local repository to your github profile
Now you have to add, commit and push your local repository to your github in order to connect this latter with AWS Codebuild for the next step. You can do these tasks either with git commands or through the source control extension available in your VS Code.

  **6.** Final checks before the setup of AWS Code Build Project

For this you should replace the `make deploy` under the build commands in the `buildspec.yml` file with the `eb deploy` command. You can also define if you want pre-build messages as they must be important in debugging phase.
Now please make sure the `config.yml` file created under the .elasticbeanstalk directroy contains the recap of the project data we entered so far in the previous steps.
Another step is to open the config file located at the `C:\Users\<YourUsername>\.aws\` directory and make sure it contains the following lines:

`[profile eb-cli]`
`region = us-east-1`
`output = json`

Please also check the content of your credentials file located under the same directory. Make sure it is of this form:

`[eb-cli]`
`aws_access_key_id = YOUR_ACCESS_KEY_ID`
`aws_secret_access_key = YOUR_SECRET_ACCESS_KEY`

  **7.** Setup AWS Code Build Project through these steps:
      1. Sign in to AWS Management Console:
            - Navigate to the AWS CodeBuild console.
      2. Create a New Build Project:
            - Click on "Create build project".
      3. Configure Project Settings:
            - Project Name: Give your project a name (e.g., FlaskElasticBeanstalkBuild).
            - Source Provider: Choose GitHub. You’ll need to authenticate with your repository  and provide the full URL of the github repository page.
      4. Environment:
            - Environment Image: Choose Managed image.
            - Operating System: Choose Amazon Linux 2.
            - Runtime: Choose Standard.
            - Image: Choose aws/codebuild/standard:5.0 or the latest available.
            - Environment Type: Choose Linux.
            - Service Role: Select New service role (or Existing service role if you already have one). AWS CodeBuild needs an IAM role to manage build actions.
      5. Buildspec:
            - Choose Use a buildspec file.
            - Ensure buildspec.yml is in the source code root.
      6. Artifacts:
            - Type: Choose No artifacts if you do not need to store the build outputs, or select Amazon S3 to store artifacts.
      7. Cache (Optional):
            - Enable caching if you want to speed up subsequent builds.
      8. Logs:
            - Enable CloudWatch logs to keep track of your build logs.
      9. Create the Project:
            - Click "Create build project" to finish creating the project.
      10. Run the build by clicking on "Start build" and wait till it complete.

There you are! Hope this works fine for you 🙂

