package wuzu.de_wuzu_project.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class WebConfig implements WebMvcConfigurer {
    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/**")  // 모든 경로 허용
                .allowedOrigins("http://<REACT_IP>:3000")  // React의 IP와 포트를 허용
                .allowedMethods("GET", "POST", "PUT", "DELETE", "OPTIONS");
    }
}
