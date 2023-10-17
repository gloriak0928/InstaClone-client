import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
// import { post } from "cypress/types/jquery";
import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
import utc from "dayjs/plugin/utc";
import InfiniteScroll from "react-infinite-scroll-component";
// import "../static/css/style.css";

dayjs.extend(relativeTime);
dayjs.extend(utc);

function Menu({ ownerImgUrl, ownerShowUrl, owner, timestamps }) {
  return (
    <div className="menu">
      <div>
        <img src={ownerImgUrl} alt="profile_image" className="profilePicture" />
        <a href={ownerShowUrl} className="userName">
          {owner}
        </a>
      </div>
      <p>{timestamps}</p>
    </div>
  );
}

function Likes({ numLikes }) {
  return (
    <form>
      <p className="Likes">{numLikes} likes</p>
    </form>
  );
}

const handleLikeClick = (
  lognameLikesThis,
  setLognameLikesThis,
  numLikes,
  setNumLikes,
  postid,
  setLikesUrl,
) => {
  const likesUrl = `/api/v1/likes/?postid=${postid}`;
  fetch(likesUrl, {
    method: "POST",
    credentials: "same-origin",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ postid }),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      setLognameLikesThis(true);
      setNumLikes(numLikes + 1);
      setLikesUrl(data.url);
    })
    .catch((error) => {
      console.error("There was a problem updating the like status:", error);
    });
  // console.log(`lognameLikesThis: ${lognameLikesThis}`);
  // console.log(`numLikes: ${numLikes}`);
  // console.log(null);
};

const handleUnlikeClick = (
  likesUrl,
  lognameLikesThis,
  setLognameLikesThis,
  numLikes,
  setNumLikes,
  postid,
  setLikesUrl,
) => {
  fetch(likesUrl, {
    method: "DELETE",
    credentials: "same-origin",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      postId: postid,
    }),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
    })
    .then(() => {
      // Update local state to reflect changes
      setLognameLikesThis(false);
      setNumLikes(numLikes - 1);
      setLikesUrl(null);
    })
    .catch((error) => {
      console.error("There was a problem updating the like status:", error);
    });
  console.log(`lognameLikesThis: ${lognameLikesThis}`);
  console.log(`numLikes: ${numLikes}`);
  console.log(likesUrl);
};

const handleNewComment = (newComment, comments, setComments, commentsurl) => {
  // setComments([...comments, newComment]);
  fetch(commentsurl, {
    method: "POST",
    credentials: "same-origin",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      text: newComment,
    }),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      // Update local state to reflect changes
      setComments([...comments, data]);
    })
    .catch((error) => {
      console.error("There was a problem updating the like status:", error);
    });
};

const handleDeleteComment = (commentid, commentsurl, comments, setComments) => {
  // setComments([...comments, newComment]);
  fetch(commentsurl, {
    method: "DELETE",
    credentials: "same-origin",
    headers: {
      "Content-Type": "application/json",
    },
    // body: JSON.stringify({
    //   text: newComment,
    // }),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
    })
    .then(() => {
      // Update local state to reflect changes
      // setComments([comments.slice(0, -1)]);
      setComments(
        comments.filter((comment) => comment.commentid !== commentid),
      );
    })
    .catch((error) => {
      console.error("There was a problem updating the like status:", error);
    });
};

function CommentsTable({ comments, setComments }) {
  return (
    <div>
      {comments.map((comment) => (
        <div
          key={comment.commentid}
          style={{ display: "flex", alignItems: "center" }}
        >
          <span key={comment.commentid} data-testid="comment-text">
            <a href={comment.ownerShowUrl} className="userName">
              {comment.owner}{" "}
            </a>
            {comment.text}
          </span>
          {comment.lognameOwnsThis && (
            <button
              type="button"
              data-testid="delete-comment-button"
              onClick={() =>
                handleDeleteComment(
                  comment.commentid,
                  comment.url,
                  comments,
                  setComments,
                )
              }
            >
              Delete Comment
            </button>
          )}
        </div>
      ))}
    </div>
  );
}

function NewComment({ addComment }) {
  // console.log("HERE")
  const [commentText, setCommentText] = useState("");

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && commentText.trim()) {
      e.preventDefault();
      addComment(commentText);
      setCommentText("");
    }
  };
  return (
    <form data-testid="comment-form">
      <input
        type="text"
        value={commentText}
        onChange={(e) => setCommentText(e.target.value)}
        onKeyDown={handleKeyDown}
      />
    </form>
  );
}

// The parameter of this function is an object with a string called url inside it.
// url is a prop for the Post component.
function Post({ url }) {
  /* Display image and post owner of a single post */

  const [imgUrl, setImgUrl] = useState("");
  const [owner, setOwner] = useState("");
  const [comments, setComments] = useState([]);
  const [timestamps, settimestamps] = useState("");
  // const [likes, setLikes] = useState({});
  const [numLikes, setNumLikes] = useState(0);
  const [lognameLikesThis, setLognameLikesThis] = useState(false);
  const [ownerImgUrl, setOwnerImgUrl] = useState("");
  const [ownerShowUrl, setOwnerShowUrl] = useState("");
  // const [postShowUrl, setPostShowUrl] = useState("");
  const [postid, setPostid] = useState(-1);
  const [likesUrl, setLikesUrl] = useState("");
  const [commentsUrl, setCommentsUrl] = useState("");

  // const [url, setUrl] = useState("")

  const onImageDoubleClick = () => {
    if (!lognameLikesThis) {
      handleLikeClick(
        lognameLikesThis,
        setLognameLikesThis,
        numLikes,
        setNumLikes,
        postid,
        setLikesUrl,
      );
    }
  };

  // const onLikeButtonClick = () => {
  //   if (!lognameLikesThis) {
  //     handleLikeClick(lognameLikesThis, setLognameLikesThis, numLikes, setNumLikes, postid, setLikesUrl);
  //   }
  // };

  useEffect(() => {
    // Declare a boolean flag that we can use to cancel the API request.
    let ignoreStaleRequest = false;

    // Call REST API to get the post's information
    fetch(url, { credentials: "same-origin" })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        // If ignoreStaleRequest was set to true, we want to ignore the results of the
        // the request. Otherwise, update the state to trigger a new render.
        if (!ignoreStaleRequest) {
          setImgUrl(data.imgUrl);
          setOwner(data.owner);
          setComments(data.comments);
          settimestamps(data.created);
          // setLikes(data.likes);
          setNumLikes(data.likes.numLikes);
          setLognameLikesThis(data.likes.lognameLikesThis);
          setOwnerImgUrl(data.ownerImgUrl);
          setOwnerShowUrl(data.ownerShowUrl);
          // setPostShowUrl(data.postShowUrl);
          setPostid(data.postid);
          setLikesUrl(data.likes.url);
          setCommentsUrl(data.commentsUrl);
        }
      })
      .catch((error) => console.log(error));

    return () => {
      // This is a cleanup function that runs whenever the Post component
      // unmounts or re-renders. If a Post is about to unmount or re-render, we
      // should avoid updating state.
      ignoreStaleRequest = true;
    };
  }, [url]);

  // Render post image and post owner
  return (
    <div className="post">
      <Menu
        ownerImgUrl={ownerImgUrl}
        ownerShowUrl={ownerShowUrl}
        owner={owner}
        timestamps={timestamps}
      />
      <img
        src={imgUrl}
        className="postImage"
        alt="post_image"
        onDoubleClick={onImageDoubleClick}
      />
      {lognameLikesThis ? (
        <button
          type="button" // Explicit type added here
          data-testid="like-unlike-button"
          onClick={() =>
            handleUnlikeClick(
              likesUrl,
              lognameLikesThis,
              setLognameLikesThis,
              numLikes,
              setNumLikes,
              postid,
              setLikesUrl,
            )
          }
        >
          unlike
        </button>
      ) : (
        <button
          type="button" // And here
          data-testid="like-unlike-button"
          className="likebutton"
          onClick={() =>
            handleLikeClick(
              lognameLikesThis,
              setLognameLikesThis,
              numLikes,
              setNumLikes,
              postid,
              setLikesUrl,
            )
          }
        >
          like
        </button>
      )}
      <Likes numLikes={numLikes} />
      <CommentsTable comments={comments} setComments={setComments} />
      <NewComment
        addComment={(comment) =>
          handleNewComment(comment, comments, setComments, commentsUrl)
        }
      />
    </div>
  );
}

export default function Posts({ url }) {
  const [results, setResults] = useState([]);
  const [next, setNext] = useState("");
  const fetchMoreData = () => {
    // if (next === "") return;
    // console.log(next);
    fetch(next, { credentials: "same-origin" })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        setResults((prevResults) => [...data.results, ...prevResults]);
        // setResults(data.results.filter(result => !results.includes(result)));
        setNext(data.next);
      })
      .catch((error) => console.log(error));
    // results.map((result)=>(
    //   console.log(result.postid)
    // ))
  };

  useEffect(() => {
    let ignoreStaleRequest = false;
    fetch(url, { credentials: "same-origin" })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        if (!ignoreStaleRequest) {
          setResults(data.results);
          setNext(data.next);
        }
      })
      .catch((error) => console.log(error));

    return () => {
      ignoreStaleRequest = true;
    };
  }, [url]);

  return (
    <div>
      {/* {results.map((result)=>(
        <Post url={result.url}/>
      ))} */}
      <InfiniteScroll
        dataLength={results.length}
        next={fetchMoreData}
        style={{ display: "flex", flexDirection: "column-reverse" }}
        hasMore={next !== ""}
        inverse={false}
        scrollThreshold={0.9}
      >
        {results.map((result) => (
          <Post key={result.postid} url={result.url} />
        ))}
      </InfiniteScroll>
    </div>
  );
}

Post.propTypes = {
  url: PropTypes.string.isRequired,
};

Posts.propTypes = {
  url: PropTypes.string.isRequired,
};

Menu.propTypes = {
  ownerImgUrl: PropTypes.string.isRequired,
  ownerShowUrl: PropTypes.string.isRequired,
  owner: PropTypes.string.isRequired,
  timestamps: PropTypes.string.isRequired,
};

Likes.propTypes = {
  numLikes: PropTypes.number.isRequired,
};

CommentsTable.propTypes = {
  comments: PropTypes.arrayOf(
    PropTypes.shape({
      commentid: PropTypes.number.isRequired,
      lognameOwnsThis: PropTypes.bool.isRequired,
      owne: PropTypes.string.isRequired,
      ownerShowUrl: PropTypes.string.isRequired,
      text: PropTypes.string.isRequired,
      url: PropTypes.string.isRequired,
    }),
  ).isRequired,
  setComments: PropTypes.func.isRequired,
};

NewComment.propTypes = {
  addComment: PropTypes.func.isRequired,
};
