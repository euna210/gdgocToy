package com.gdgoc.backend.posting.entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;
import lombok.NoArgsConstructor;

import java.time.LocalDate;

@Entity
@Table(name = "postings")
@Getter
@Setter
@NoArgsConstructor
public class Posting {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String type;

    @Column(nullable = false)
    private String title;

    private String organizer;

    private LocalDate applyStart;

    private LocalDate deadline;

    @Column(nullable = false)
    private String deadlineType;

    private String deadlineNote;

    private String link;

    @Column(length = 2000)
    private String summary;

    private Integer minGrade;

    private Integer maxGrade;

    private String benefits;

    private String activityPeriod;

    private String participation;

    private String mode;
}