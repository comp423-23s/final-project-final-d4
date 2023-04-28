# Post

## Overview
The post forum feature provides functionality for viewing posts, creating posts, searching for posts, and deleting posts in the post forum. This feature fulfills **four** stories in our project, including view-post story, create-post story, search-post story, and delete-post story. It primarily serves to **UNC students who are looking for potential projects to get involved in or students who have project ideas in mind and are looking for teammates to build the project together**. 

This feature is the primary feature in our final project and would make the UNC CS community more cooperative and innovative. Details are as below:

## Post Elements
Each post has following elements:
* **id**: An unique id assigned automatically to each post when creating.
* **pid**: The PID of the author of the post.
* **title**: The title of the post. The title can be simple, such as "Finding teammate: backend" or "Random thoughts about ChatGPT".
* **description**: A breif summary of the post, for example, "I found this interesting paper on ChatGPT talking about its possible applications".
* **content**: The detailed content of the post.
* **tags**: Tags are similar to hashtags on social media that can be added to posts.
* **created**: The time the post is created.

## Read Posts
![Untitled design](https://user-images.githubusercontent.com/69743708/235230400-61b45aa2-33bd-4659-a251-724e4ad7af87.gif)



* **Usage**: The goal of this function is to view a list of posts and a detailed page of a post. The user can enter the list of posts page by clicking the "Projects" on the left navigation bar. And the user can see details including comments of a specific post by clicking the card of a post.

* **Permission**:All users can browse posts after authentication. 


## Create Posts
![Untitled design (1)](https://user-images.githubusercontent.com/69743708/235233007-4e34d853-6088-4301-a561-45c73a34cb64.gif)

* **Usage**: The goal of this function is to create and public a post. A CSXL user could create a post by navigating to create-post in the post forum. The user should enter the post title, description, content, and choose tags to create a post. Title, description, and content are required. If one of thse is empty, the frame of the cell will turn red, and clickling the Create Post button will have no response.

* **Permission**: Only registered users can create posts.

## Search Posts
![Untitled design (2)](https://user-images.githubusercontent.com/69743708/235233452-cbd7b667-4efb-46d6-ac5a-537134f8f816.gif)

* **Usage**: The goal of this function is to allow user to search for specif posts they are interested in. CSXL user could search specific posts using the search bar on the top and type keywords they want. 

* **Permission**: All users can search posts in the post tab after authentication. 

## Edit Posts
![Untitled design (4)](https://user-images.githubusercontent.com/69743708/235234781-e3506761-92cb-44a5-ae27-e453a8e11468.gif)

* **Usage**: The goal of this function is to allow the author of a post to edit the post. The author of the post can edit the post by clicking the Edit button on the top right corner in the detailed post page.

* **Permission**: Only two types of users can edit a posts: the author of the post or the administrator.

## Delete Posts
![Untitled design (3)](https://user-images.githubusercontent.com/69743708/235234774-255e02ec-2a71-45fc-abff-6aa9f4f7f2ef.gif)

* **Usage**: The goal of this function is to permanantly delete a post including comments of the post. CSXL users could delete their own posts in the post forum if they click on the black trash bin button. 

* **Permission**: Only two types of users can delete a posts: the author of the post or the administrator.



## Implementation Notes
This feature is associated with a post table (backend/entities/post_entities). Each post has features such as content, tags, created time, title, and descriptions.  

One of the interesting design points is tags. We thought about our experiences on other platforms and found that it is useful for viewers to find specific categories of posts they want if the author of a post can tag the post initially. For example, if a user wants to join an existing team for a project, the user can search for the tag "Finding teammates". Every post with this tag will appear, making it easier for the user to find what they are looking for. We have some predefined tags such as "finding teammates", "share insights", "backend", "frontend". We chose to use tags instead of letting users search posts by contents or titles because we understand that people would have different wording for the same thing. The tag can unify the wording and make it easier for users to retrieve the information they want.

## Development Concerns
**Please do not create a post if you have not yet registered in CSXL!** The create-post function depends on a registered user, and the action should result in a HTTP error if the user is not yet registered!

Other than that, be aware of the following things:
* Backend: 
1. The backend implementation of the post forum feature is in api/post.py and services/post.py. The create_post service function takes a NewPost model from the frontend post form, which only has content, tags, created, datetime, title, and description. The create_post function will take parameters from the NewPost model and construct a Post model for passing into the post table. The Post model has information about the user who creates the post by extracting from the /authentication/registered user.
2. There is a permission check in the delete_post method. If the subject is not the user who created the post, the permission service would check whether the subject has permission to delete the post. Only the administrator who has the post.delete action permission would delete other users' posts.
* Frontend:
1. The frontend implementation of the post feature is in the [post-list component](https://github.com/comp423-23s/final-project-final-d4/tree/stage/frontend/src/app/post-list), [create-post component](https://github.com/comp423-23s/final-project-final-d4/tree/stage/frontend/src/app/create-post), and [post.service.ts](https://github.com/comp423-23s/final-project-final-d4/blob/stage/frontend/src/app/post.service.ts).  
2. There are 2 permission checks in the delete post sub-feature of the frontend. **deleteAdminPermission$** is an Observable<Boolean> checks whether the authenticated user has permission to delete user people's posts. It interacts with the check method of the permission service to fetch permission information. [The delete button for administrator only appears if the boolean variable is true](https://github.com/comp423-23s/final-project-final-d4/blob/02ac2feea0af519d223566723c4170c53cffb076/frontend/src/app/post-list/post-list.component.html#L23). The second permission check is implemented via **getDeleteUserPermission()** function in post-list.component.ts. It takes the pid associated with the specific post and calls [checkPID(PID: number)](https://github.com/comp423-23s/final-project-final-d4/blob/02ac2feea0af519d223566723c4170c53cffb076/frontend/src/app/permission.service.ts#L29) in the permission service. This method returns true if the postPID and the PID of the CSXL user are equal.
3. The same thing is implemented in edit post. **editAdminPermission$** is an Observable<Boolean> checks whether the authenticated user has permission to edit people's posts. It interacts with the check method of the permission service to fetch permission information. [The edit button for administrator only appears if the boolean variable is true](https://github.com/comp423-23s/final-project-final-d4/blob/75c91244c8d7dd1c2dea36216862a393879bb10e/frontend/src/app/post-details/post-details.component.html#L28). The second permission check is implemented via **getEditUserPermission()** function in post-details.component.ts. It takes the pid associated with the specific post and calls [checkPID(PID: number)](https://github.com/comp423-23s/final-project-final-d4/blob/02ac2feea0af519d223566723c4170c53cffb076/frontend/src/app/permission.service.ts#L29) in the permission service. This method returns true if the postPID and the PID of the CSXL user are equal.
4. The create-post sub-feature sends the NewPost model to the backend via HTTP POST request. All methods with HTTP concerns in the post service takes PostView model as a return object. NewPost matches NewPost model in the backend while PostView Matches Post model in the backend. 

## Future Work
Developers can add more interaction functions to the post feature, for example the like/dislike button, or a bookmark symbol that allows the user to bookmark a post.
