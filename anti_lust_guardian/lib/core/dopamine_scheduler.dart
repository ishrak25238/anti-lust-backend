import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

class DopamineScheduler {
  static const String _startTimeKey = 'detox_start_time';
  static const String _endTimeKey = 'detox_end_time';
  static const String _isEnabledKey = 'detox_enabled';

  Future<void> setSchedule(TimeOfDay start, TimeOfDay end, bool enabled) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setInt(_startTimeKey, _timeToMinutes(start));
    await prefs.setInt(_endTimeKey, _timeToMinutes(end));
    await prefs.setBool(_isEnabledKey, enabled);
  }

  Future<bool> isScrollBlocked() async {
    final prefs = await SharedPreferences.getInstance();
    final enabled = prefs.getBool(_isEnabledKey) ?? false;
    if (!enabled) return false;

    final startMinutes = prefs.getInt(_startTimeKey);
    final endMinutes = prefs.getInt(_endTimeKey);

    if (startMinutes == null || endMinutes == null) return false;

    final now = TimeOfDay.now();
    final nowMinutes = _timeToMinutes(now);

    if (startMinutes < endMinutes) {
      return nowMinutes >= startMinutes && nowMinutes <= endMinutes;
    } else {
      return nowMinutes >= startMinutes || nowMinutes <= endMinutes;
    }
  }

  int _timeToMinutes(TimeOfDay time) {
    return time.hour * 60 + time.minute;
  }
}
