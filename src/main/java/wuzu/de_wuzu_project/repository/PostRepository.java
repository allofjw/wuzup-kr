package wuzu.de_wuzu_project.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import wuzu.de_wuzu_project.domain.Post;

import java.time.LocalDate;
import java.time.LocalTime;
import java.util.List;

public interface PostRepository extends JpaRepository<Post, Long> {
    // 특정 날짜의 오전 데이터 조회
    @Query("SELECT p FROM Post p WHERE p.date = :date AND p.time < :noon")
    List<Post> findMorningPostsByDate(@Param("date") LocalDate date, @Param("noon") LocalTime noon);

    @Query("SELECT p FROM Post p WHERE p.date = :date AND p.time >= :noon")
    List<Post> findAfternoonPostsByDate(@Param("date") LocalDate date, @Param("noon") LocalTime noon);

    @Query("SELECT p FROM Post p")
    List<Post>findAll();

    @Query("SELECT p FROM Post p JOIN FETCH p.keywords")
    List<Post> findAllWithKeywords();

    List<Post> findByDate(LocalDate date);

}
