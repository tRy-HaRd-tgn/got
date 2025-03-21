import styles from "./styles.module.scss";
import { Header, Footer, News } from "../../components";
import { useEffect } from "react";
import PostService from "../../services/PostService";
import { useSelector, useDispatch } from "react-redux";
import { news, rectangles, vector } from "../../imgs";
export const Blog = () => {
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
        <img className={styles.img} src={news} alt="error" />
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
      <div className={styles.project}>
        <img
          style={{ zIndex: 99 }}
          className={styles.img}
          src={rectangles}
          alt=""
        />
      </div>
      <Footer />
    </main>
  );
};
