//  Copyright (c) 2019-present, VidarDB, Inc.  All rights reserved.
//  This source code is licensed under the BSD-style license found in the
//  LICENSE file in the root directory of this source tree. An additional grant
//  of patent rights can be found in the PATENTS file in the same directory.
//
// Copyright (c) 2011-present, Facebook, Inc.  All rights reserved.
// This source code is licensed under the BSD-style license found in the
// LICENSE file in the root directory of this source tree. An additional grant
// of patent rights can be found in the PATENTS file in the same directory.

#pragma once

#include <string>
#include <vector>

#include "vidardb/options.h"
#include "vidardb/splitter.h"

namespace vidardb {

// ImmutableCFOptions is a data struct used by VidarDB internal. It contains a
// subset of Options that should not be changed during the entire lifetime
// of DB. You shouldn't need to access this data structure unless you are
// implementing a new TableFactory. Raw pointers defined in this struct do
// not have ownership to the data they point to. Options contains shared_ptr
// to these data.
struct ImmutableCFOptions {
  explicit ImmutableCFOptions(const Options& options);

  CompactionStyle compaction_style;

  CompactionOptionsFIFO compaction_options_fifo;

  const Comparator* comparator;

  const Splitter* splitter;

  Logger* info_log;

  Statistics* statistics;

  InfoLogLevel info_log_level;

  Env* env;

  uint64_t delayed_write_rate;

  // Allow the OS to mmap file for reading sst tables. Default: false
  bool allow_mmap_reads;

  // Allow the OS to mmap file for writing. Default: false
  bool allow_mmap_writes;

  std::vector<DbPath> db_paths;

  MemTableRepFactory* memtable_factory;

  TableFactory* table_factory;

  Options::TablePropertiesCollectorFactories
    table_properties_collector_factories;

  bool advise_random_on_open;

  bool purge_redundant_kvs_while_flush;

  bool disable_data_sync;

  bool use_fsync;

  std::vector<CompressionType> compression_per_level;

  CompressionType bottommost_compression;

  CompressionOptions compression_opts;

  Options::AccessHint access_hint_on_compaction_start;

  bool new_table_reader_for_compaction_inputs;

  size_t compaction_readahead_size;

  int num_levels;

  // A vector of EventListeners which call-back functions will be called
  // when specific VidarDB event happens.
  std::vector<std::shared_ptr<EventListener>> listeners;

  std::shared_ptr<Cache> row_cache;
};

}  // namespace vidardb
