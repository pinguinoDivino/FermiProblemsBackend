
AVOID_DUPLICATES = True


def calculate_score_from_logs(logs, problem_ids):
    if AVOID_DUPLICATES:
        scores = []
        for problem_id in problem_ids:
            problem_id = str(problem_id)
            _winner = None
            _score = None
            for log in logs:
                if _score and not log.text[problem_id][0]['time_out'] and \
                        abs(log.text[problem_id][0]['value'] - log.text[problem_id][0]['correct_value']) < _score:
                    _score = log.text[problem_id][0]['value']
                    _winner = log.player
                elif log.text[problem_id][0]['time_out']:
                    pass
                else:
                    # TODO Errore vince chi va in timeout?
                    _score = log.text[problem_id][0]['value']
                    _winner = log.player
            scores.append(_winner)

        return max(set(scores), key=scores.count)
    else:
        return logs[0].player

