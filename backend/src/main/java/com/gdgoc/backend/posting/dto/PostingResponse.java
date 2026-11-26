package com.gdgoc.backend.posting.dto;

import com.gdgoc.backend.posting.entity.Posting;
import java.time.LocalDate;

public record PostingResponse(
        Long id,
        String type,
        String title,
        String organizer,
        LocalDate apply_start,
        LocalDate deadline,
        String deadline_type,
        String deadline_note,
        String link,
        String summary,
        Integer min_grade,
        Integer max_grade,
        String benefits,
        String activity_period,
        String participation,
        String mode
) {
    public static PostingResponse from(Posting posting) {
        return new PostingResponse(
                posting.getId(),
                posting.getType(),
                posting.getTitle(),
                posting.getOrganizer(),
                posting.getApplyStart(),
                posting.getDeadline(),
                posting.getDeadlineType(),
                posting.getDeadlineNote(),
                posting.getLink(),
                posting.getSummary(),
                posting.getMinGrade(),
                posting.getMaxGrade(),
                posting.getBenefits(),
                posting.getActivityPeriod(),
                posting.getParticipation(),
                posting.getMode()
        );
    }
}