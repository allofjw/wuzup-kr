package wuzu.de_wuzu_project.domain;

import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDate;
import java.time.LocalTime;
import java.util.ArrayList;
import java.util.List;

@Entity
@AllArgsConstructor
@NoArgsConstructor
@Getter @Setter
public class Post {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String title;
    private String topic;

    @ElementCollection(fetch = FetchType.LAZY) // Lazy로 가져오지만 필요 시 같이 조회 가능
    @CollectionTable(name = "post_keywords", joinColumns = @JoinColumn(name = "post_id"))
    @Column(name = "keyword")
    private List<String> keywords = new ArrayList<>();
    @Column(nullable = false)
    private LocalDate date = LocalDate.now(); // 기본값 설정

    @Column(nullable = false)
    private LocalTime time = LocalTime.now(); // 기본값 설정

}
