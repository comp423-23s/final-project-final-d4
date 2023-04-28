# Comments

## Authors: Wenjing Huang, Chalisa "Keaw" Phoomsakha, Guning Shen, Ziqian Zhao

## Overview
The comment feature provides functionality for viewing, creating and deleting comments on posts. It primarily serves for users who are interested in the post and wants to discuss with other users. This feature allows the community to be more interactive and friendly.

Details are as below:

## Comment Elements
Each comment has following elements:
* **id**: An unique id assigned automatically to each comment when creating.
* **commenter**: The PID of the author of the comment.
* **post**: The id of the post that the comment is under.
* **text**: The detailed content of the comment.
* **private**: An indicator of the privacy of the comment.
* **created**: The time the post is created.

## Read Comments
![Untitled design (5)](https://user-images.githubusercontent.com/69743708/235239010-c0ec154a-ade9-48b7-b1ed-965bc101fc1a.gif)

* **Usage**: The goal of this function is to view a list of comments of a post. The user can can see comments of a specific post by clicking the card of a post in the projects tab.

* **Permission**:All users can browse **public** comments after authentication. If a comment is **private**, only the author of the post, the author of the comment, and the admin can see it.


## Create Comments
![Untitled design (6)](https://user-images.githubusercontent.com/69743708/235240500-2bb0da20-032e-4021-ae9c-6ca2b8503f54.gif)

* **Usage**: The goal of this function is to create and public a comment. A CSXL user could create a comment by navigating to detailed page of a post. The user should enter the comment text and choose wither private or public to create a post. The text entry and the private/public choice are required. If either is empty, clickling the Add Comment button will have no response.

* **Permission**: Only registered users can create comments.

## Delete Comments
![Untitled design (8)](https://user-images.githubusercontent.com/69743708/235241054-7a62f730-2279-4d61-9911-1b0abe0872ce.gif)

* **Usage**: The goal of this function is to permanantly delete acomment. CSXL users could delete their own comments under a post if they click on the black trash bin button. 

* **Permission**: Only two types of users can delete a comment: the author of the comment or the administrator.

## Implementation Notes
This feature is associated with a comment table (backend/entities/comment_entity). Each comment has features such as text and private.  

And the interesting design choice is the private indicator. We thought about the possibility that when a post is about finding teammates for project, it is not cyberly safe for users to type their information in the comment publicly. We choose to add a private feature to comments over adding a communication system to the website becuase we know most people still prefer to communicate using texts, slack, and other ways. By allowing users to create private comments, they can exchange their information safely.

## Development Concerns
Be aware of the following points when making progress:

* Backend
1. The backend implementation of the comment feature is in api/comment.py and services/comment.py. The create service function takes a NewComment model from the frontend comment form, which only has id, text, created, and private. The create function will take parameters from the NewComment model and construct a Comment model for passing into the comment table. The Comment model has information about the user who creates the comment by extracting from the /authentication/registered user.
2. There is a permission check in the delete_comment method. If the subject is not the user who created the post or the author of the comment, the permission service would check whether the subject has permission to delete the comment. Only the administrator who has the comment.delete action permission would delete other users' comments.

* Frontend
1. The frontend implementation is in [post-details component](https://github.com/comp423-23s/final-project-final-d4/tree/stage/frontend/src/app/post-details), and [comment.service.ts](https://github.com/comp423-23s/final-project-final-d4/blob/stage/frontend/src/app/comment.service.ts). 
2. There is a permission check needed for viewing comments. Each comment will only be visible to the current user if **visibleComment(comment)** is true. It returns a Observable<Boolean> checks whether the authenticated user has permission to see this comment. It interacts with the check method of the permission service to fetch permission information. And it checks whether the registered user is the author of the post or the author of the comment.
3. There are 2 permission checks in the delete comment sub-feature of the frontend. **deleteAdminPermission$** is an Observable<Boolean> checks whether the authenticated user has permission to delete users' comments. It interacts with the check method of the permission service to fetch permission information. [The delete button for administrator only appears if the boolean variable is true](https://github.com/comp423-23s/final-project-final-d4/blob/02ac2feea0af519d223566723c4170c53cffb076/frontend/src/app/post-list/post-list.component.html#L23). The second permission check is implemented via **getDeleteUserPermission()** function in post-details.component.ts. It takes the pid associated with the specific post and calls [checkPID(PID: number)](https://github.com/comp423-23s/final-project-final-d4/blob/02ac2feea0af519d223566723c4170c53cffb076/frontend/src/app/permission.service.ts#L29) in the permission service. This method returns true if the commenterPID and the PID of the CSXL user are equal.
4. The create-comment sub-feature sends the NewComment model to the backend via HTTP POST request. All methods with HTTP concerns in the comment service takes Comment model as a return object. newComment matches NewComment model in the backend while Comment matches Comment model in the backend.

## Future Work
The comment feature can be more interesting if we can add reactions such as like or dislike just like a forum. Given more time, we would add this feature in it.
You can also add reply to comments when you get started to make it more interactive.

