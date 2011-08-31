# Generated by jeweler
# DO NOT EDIT THIS FILE DIRECTLY
# Instead, edit Jeweler::Tasks in Rakefile, and run 'rake gemspec'
# -*- encoding: utf-8 -*-

Gem::Specification.new do |s|
  s.name = %q{karait}
  s.version = "0.0.1"

  s.required_rubygems_version = Gem::Requirement.new(">= 0") if s.respond_to? :required_rubygems_version=
  s.authors = ["bcoe"]
  s.date = %q{2011-08-31}
  s.description = %q{A ridiculously simple cross-language queuing system, built on top of MongoDB.}
  s.email = %q{bencoe@gmail.com}
  s.extra_rdoc_files = [
    "README.markdown"
  ]
  s.files = [
    ".gitignore",
    "Gemfile",
    "Gemfile.lock",
    "LICENSE.txt",
    "README.markdown",
    "Rakefile",
    "VERSION",
    "lib/karait.rb",
    "lib/message.rb",
    "lib/queue.rb",
    "test/helper.rb",
    "test/test_message.rb",
    "test/test_queue.rb"
  ]
  s.homepage = %q{http://github.com/bcoe/karait}
  s.licenses = ["MIT"]
  s.require_paths = ["lib"]
  s.rubygems_version = %q{1.4.2}
  s.summary = %q{A ridiculously simple cross-language queuing system, built on top of MongoDB.}

  if s.respond_to? :specification_version then
    s.specification_version = 3

    if Gem::Version.new(Gem::VERSION) >= Gem::Version.new('1.2.0') then
    else
    end
  else
  end
end
