package com.gdgoc.backend;

import com.gdgoc.backend.posting.entity.Posting;
import com.gdgoc.backend.posting.repository.PostingRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import java.time.LocalDate;

@Component
public class DataInitializer implements CommandLineRunner {

    private final PostingRepository postingRepository;

    public DataInitializer(PostingRepository postingRepository) {
        this.postingRepository = postingRepository;
    }

    @Override
    public void run(String... args) {
        if (postingRepository.count() == 0) {
            Posting posting = new Posting();

            posting.setType("공모전");
            posting.setTitle("대학생 AI 아이디어 공모전");
            posting.setOrganizer("GDGoC");
            posting.setDeadline(LocalDate.of(2026, 12, 20));
            posting.setDeadlineType("날짜");
            posting.setSummary("대학생 대상 AI 아이디어 공모전입니다.");

            postingRepository.save(posting);
        }
    }
}