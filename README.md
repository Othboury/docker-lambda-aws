# docker-lambda-aws
Project to highlight creating an AWS Lambda function with Python and pushing it via Docker.

AWS give the opportunity to create Lambda Fubcrion in order to perform different task on the cloud. Lambda functions are triggered by events (example: An upload to S3 Bucket), after the excution of the lambda fucntion we're able to trigger another behaviour (example: Sending notifcation to mobile using Amazon SNS).

In this example, and sice it was used in a Machine Learning project, we're triggering a lambda function after every file into the S3 Bucket using Python. We first get the object (The ML model) from the bucket and do the prediction inside the lambda funtion before returning it in the body of a JSON response.

The tricky part about using Python is that in order to execute the code we're obliged to import multiple librairies. These librairies are either added to the lambda fucntion as layers by pip installing them via AWS CLOUD9. The issues is that the size of layers is limited and we can't import may librairies, especially the heavy ones.

To get pass this issue, we gonna upload the lambda handler file and the librairies mentionned in requirement.txt using Docker.

AWS ECR gives us the posiibility to create containers and upload docker images into it.

The steps to do so are:

1. Creating the lambda handler file
2. Creating the requirement.txt file
3. Creating the docker file
4. Creating a container in AWS ECR
5. Applying the push commands given by Amazon in order to build an image and push it to the container
