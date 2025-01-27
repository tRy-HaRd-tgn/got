import styles from "./styles.module.scss";
import { Header, Footer } from "../../components";
import { vector } from "../../imgs";
import { useEffect } from "react";
import { News } from "../../components";
import PostService from "../../services/PostService";
import { useSelector, useDispatch } from "react-redux";

export const Blog = (props) => {
  const dispatch = useDispatch();
  const setNews = (news) => {
    dispatch({ type: "SET_NEWS", news: news });
  };
  const pickNews = async (e) => {
    try {
      const responce = await PostService?.getPosts();
      setNews(responce.data);
    } catch {
      console.log(e.responce?.data?.message);
    }
  };
  useEffect(() => {
    pickNews();
  }, []);
  const data = useSelector((state) => state.news.news);
  return (
    <main className={styles.main}>
      <Header />
      <div className={styles.description}>
        <h1 style={{ marginTop: "20vh" }}>новости проекта</h1>
      </div>
      <div className={styles.newsWrapper}>
        {data.map((value, index) => (
          <News
            id={value.id}
            img={value.image_url}
            key={index}
            header={value.title}
            author={value.author_login}
            data={value.created_at}
            text={value.content}
            url={value.discord_url}
          />
        ))}
      </div>
      <img src={vector} alt="" className={styles.devider} />

      <div className={styles.project}></div>
      <Footer />
    </main>
  );
};
